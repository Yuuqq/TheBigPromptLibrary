# Dynarmic 设计文档

Dynarmic 是一个用于 ARMv6K 架构的动态重编译器。Dynarmic 的未来计划包括支持其他版本的 ARM 架构、拥有解释器模式以及添加对其他架构的支持。

本库的用户主要通过 [`src/dynarmic/interface`](../src/dynarmic/interface) 中提供的接口与之交互。用户通过提供相关 `UserCallbacks` 接口的实现来指定 dynarmic 的 CPU 核心如何与其系统的其余部分交互。用户使用 `Jit` 的成员函数设置 CPU 状态，然后调用 `Jit::Execute` 开始 CPU 执行。在 `UserCallbacks` 上定义的回调可能从动态生成的代码中调用，因此库的用户不应依赖于堆栈处于可用于展开的可遍历状态。

* A32: [`Jit`](../src/dynarmic/interface/A32/a32.h), [`UserCallbacks`](../src/dynarmic/interface/A32/config.h)
* A64: [`Jit`](../src/dynarmic/interface/A64/a64.h), [`UserCallbacks`](../src/dynarmic/interface/A64/config.h)

Dynarmic 通过调用 `UserCallbacks::MemoryReadCode` 从内存中读取指令。这些指令然后经过几个阶段：

1. 解码（识别指令类型并将其分解为字段）
2. 翻译（从指令生成高级 IR）
3. 优化（消除冗余微指令，其他速度改进）
4. 发射（将主机可执行代码生成到内存中）
5. 执行（主机 CPU 跳转到发射代码的开始并运行它）

以 A32 前端和 x64 后端为例：

* 解码通过 [`src/frontend/A32/decoder/{arm.h,thumb16.h,thumb32.h}`](../src/dynarmic/frontend/A32/decoder/) 中的[双重分派](https://en.wikipedia.org/wiki/Visitor_pattern)完成。
* 翻译由 [`src/dynarmic/frontend/A32/translate/translate_{arm,thumb}.cpp`](../src/dynarmic/frontend/A32/translate/) 中的访问者完成。函数 [`Translate`](../src/dynarmic/frontend/A32/translate/translate.h) 接受起始内存位置、一些 CPU 状态和内存读取回调，并返回 IR 的基本块。
* IR 可以在 [`src/frontend/ir/`](../src/dynarmic/ir/) 下找到。
* 优化可以在 [`src/ir_opt/`](../src/dynarmic/ir/opt/) 下找到。
* 发射由 `EmitX64` 完成，可以在 [`src/dynarmic/backend/x64/emit_x64.{h,cpp}`](../src/dynarmic/backend/x64/) 中找到。
* 执行通过调用 [`src/dynarmic/backend/x64/block_of_code.{h,cpp}`](../src/dynarmic/backend/x64/) 中的 `BlockOfCode::RunCode` 来执行。

## 解码器

解码器是一个双重分派解码器。每条指令由相关指令表中的一行表示。以下是来自 [`arm.h`](../src/dynarmic/frontend/A32/decoder/arm.h) 的示例行：

    INST(&V::arm_ADC_imm,     "ADC (imm)",           "cccc0010101Snnnnddddrrrrvvvvvvvv")

（有关此指令的详细信息可以在 ARMv7-A 手册的 A8.8.1 节中找到。这是编码 A1。）

INST 的第一个参数是要在访问者上调用的成员函数。第二个参数是人类可读的指令名称。第三个参数是指令的位表示。

### 指令位表示

位字符串中的每个字符代表一个位。`0` 表示该位位置**必须**包含零。`1` 表示该位位置**必须**包含一。`-` 表示我们不关心该位位置的值。相同字符的字符串代表一个字段。在上面的例子中，前四位 `cccc` 代表 ARM 带进位加法（立即数）指令的四位长 cond 字段。

访问者必须有一个名为 `arm_ADC_imm` 的函数，带有 6 个参数，每个字段一个（`cccc`、`S`、`nnnn`、`dddd`、`rrrr`、`vvvvvvvv`）。如果字段数量与参数数量不匹配，将导致编译时错误。

## 翻译器

翻译器是一个使用解码器来解码指令的访问者。翻译器借助 [`IREmitter` 类](../src/dynarmic/ir/ir_emitter.h)生成 IR 代码。以下是翻译函数的示例：

```cpp
bool ArmTranslatorVisitor::arm_ADC_imm(Cond cond, bool S, Reg n, Reg d, int rotate, Imm8 imm8) {
    u32 imm32 = ArmExpandImm(rotate, imm8);

    // ADC{S}<c> <Rd>, <Rn>, #<imm>

    if (ConditionPassed(cond)) {
        auto result = ir.AddWithCarry(ir.GetRegister(n), ir.Imm32(imm32), ir.GetCFlag());

        if (d == Reg::PC) {
            ASSERT(!S);
            ir.ALUWritePC(result.result);
            ir.SetTerm(IR::Term::ReturnToDispatch{});
            return false;
        }

        ir.SetRegister(d, result.result);
        if (S) {
            ir.SetNFlag(ir.MostSignificantBit(result.result));
            ir.SetZFlag(ir.IsZero(result.result));
            ir.SetCFlag(result.carry);
            ir.SetVFlag(result.overflow);
        }
    }

    return true;
}
```

其中 `ir` 是 `IRBuilder` 类的实例。`IRBuilder` 类的每个成员函数构造一个 IR 微指令。

## 中间表示

Dynarmic 使用有序 SSA 中间表示。它与其他类似项目（如 redream、nucleus 和 xenia）中的表示非常相似。主要区别是：（1）上下文微指令的丰富程度，而那些项目通常只有两个（`load_context`/`store_context`），（2）将标志显式处理为它们自己的值，以及（3）非常不同的基本块边缘处理。

上下文微指令和显式标志处理的目的是允许未来的优化。边缘处理方式的差异是当前实现的一个怪癖，dynarmic 可能会在中期未来添加函数分析器。

Dynarmic 的中间表示是有类型的。每个微指令可以接受零个或多个参数，并可能返回零个或多个参数。下面记录了可用微指令的子集。

完整的微指令列表可以在 [src/dynarmic/ir/opcodes.inc](../src/dynarmic/ir/opcodes.inc) 中找到。

下面列出了一些常用的微指令。

### 立即数: Imm{U1,U8,U32,RegRef}

    <u1> ImmU1(u1 value)
    <u8> ImmU8(u8 value)
    <u32> ImmU32(u32 value)
    <RegRef> ImmRegRef(Arm::Reg gpr)

这些指令接受 `bool`、`u8` 或 `u32` 值并将其包装在 IR 节点中，以便它们可以被 IR 使用。

### 上下文: {Get,Set}Register

    <u32> GetRegister(<RegRef> reg)
    <void> SetRegister(<RegRef> reg, <u32> value)

获取和设置 `JitState::Reg[reg]`。注意 `SetRegister(Arm::Reg::R15, _)` 被 IRBuilder 禁止。请改用 `{ALU,BX}WritePC`。

注意像 `SetRegister(R4, _)` 后跟 `GetRegister(R4)` 这样的序列会被优化掉。

### 上下文: {Get,Set}{N,Z,C,V}Flag

    <u1> GetNFlag()
    <void> SetNFlag(<u1> value)
    <u1> GetZFlag()
    <void> SetZFlag(<u1> value)
    <u1> GetCFlag()
    <void> SetCFlag(<u1> value)
    <u1> GetVFlag()
    <void> SetVFlag(<u1> value)

获取和设置 `JitState::Cpsr` 中的位。与寄存器类似，冗余的 get/set 会被优化掉。

### 上下文: BXWritePC

    <void> BXWritePC(<u32> value)

除非你正在做一些花哨的事情，否则这应该是翻译块中的最后一条指令。

此微指令根据需要设置 R15 和 CPSR.T。

### 回调: CallSupervisor

    <void> CallSupervisor(<u32> svc_imm32)

除非你正在做一些花哨的事情，否则这应该是翻译块中的最后一条指令。

### 计算: LastSignificant{Half,Byte}

    <u16> LeastSignificantHalf(<u32> value)
    <u8> LeastSignificantByte(<u32> value)

分别从 u32 中提取 u16 和 u8。

### 计算: MostSignificantBit, IsZero

    <u1> MostSignificantBit(<u32> value)
    <u1> IsZero(<u32> value)

这些用于实现 ARM 标志 N 和 Z。这些通常可以被后端优化为主机标志读取。

### 计算: LogicalShiftLeft

    (<u32> result, <u1> carry_out) LogicalShiftLeft(<u32> operand, <u8> shift_amount, <u1> carry_in)

伪代码：

        if shift_amount == 0:
            return (operand, carry_in)

        x = operand * (2 ** shift_amount)
        result = Bits<31,0>(x)
        carry_out = Bit<32>(x)

        return (result, carry_out)

这遵循 ARM 语义。注意 `shift_amount` 不会被掩码为 5 位（如 x64 上的 `SHL` 那样）。

### 计算: LogicalShiftRight

    (<u32> result, <u1> carry_out) LogicalShiftLeft(<u32> operand, <u8> shift_amount, <u1> carry_in)

伪代码：

        if shift_amount == 0:
            return (operand, carry_in)

        x = ZeroExtend(operand, from_size: 32, to_size: shift_amount+32)
        result = Bits<shift_amount+31,shift_amount>(x)
        carry_out = Bit<shift_amount-1>(x)

        return (result, carry_out)

这遵循 ARM 语义。注意 `shift_amount` 不会被掩码为 5 位（如 x64 上的 `SHR` 那样）。

### 计算: ArithmeticShiftRight

    (<u32> result, <u1> carry_out) ArithmeticShiftRight(<u32> operand, <u8> shift_amount, <u1> carry_in)

伪代码：

        if shift_amount == 0:
            return (operand, carry_in)

        x = SignExtend(operand, from_size: 32, to_size: shift_amount+32)
        result = Bits<shift_amount+31,shift_amount>(x)
        carry_out = Bit<shift_amount-1>(x)

        return (result, carry_out)

这遵循 ARM 语义。注意 `shift_amount` 不会被掩码为 5 位（如 x64 上的 `SAR` 那样）。

### 计算: RotateRight

    (<u32> result, <u1> carry_out) RotateRight(<u32> operand, <u8> shift_amount, <u1> carry_in)

伪代码：

        if shift_amount == 0:
            return (operand, carry_in)

        shift_amount %= 32
        result = (operand << shift_amount) | (operand >> (32 - shift_amount))
        carry_out = Bit<31>(result)

        return (result, carry_out)

### 计算: AddWithCarry

    (<u32> result, <u1> carry_out, <u1> overflow) AddWithCarry(<u32> a, <u32> b, <u1> carry_in)

a + b + carry_in

### 计算: SubWithCarry

    (<u32> result, <u1> carry_out, <u1> overflow) SubWithCarry(<u32> a, <u32> b, <u1> carry_in)

这与 `AddWithCarry(a, Not(b), carry_in)` 具有等效语义。

a - b - !carry_in

### 计算: And

    <u32> And(<u32> a, <u32> b)

### 计算: Eor

    <u32> Eor(<u32> a, <u32> b)

异或（即：XOR）

### 计算: Or

    <u32> Or(<u32> a, <u32> b)

### 计算: Not

    <u32> Not(<u32> value)

### 回调: {Read,Write}Memory{8,16,32,64}

    <u8> ReadMemory8(<u32> vaddr)
    <u8> ReadMemory16(<u32> vaddr)
    <u8> ReadMemory32(<u32> vaddr)
    <u8> ReadMemory64(<u32> vaddr)
    <void> WriteMemory8(<u32> vaddr, <u8> value_to_store)
    <void> WriteMemory16(<u32> vaddr, <u16> value_to_store)
    <void> WriteMemory32(<u32> vaddr, <u32> value_to_store)
    <void> WriteMemory64(<u32> vaddr, <u64> value_to_store)

内存访问。

### 终端: Interpret

    SetTerm(IR::Term::Interpret{next})

此终端指令调用解释器，从 `next` 开始。解释器必须精确解释一条指令。

### 终端: ReturnToDispatch

    SetTerm(IR::Term::ReturnToDispatch{})

此终端指令将控制权返回给调度器。调度器将使用 R15 中的值来确定下一步。

### 终端: LinkBlock

    SetTerm(IR::Term::LinkBlock{next})

如果我们有足够的剩余周期，此终端指令跳转到由 `next` 描述的基本块。如果我们没有足够的剩余周期，我们返回调度器，调度器将控制权返回给主机。

### 终端: PopRSBHint

    SetTerm(IR::Term::PopRSBHint{})

此终端指令根据 R15 检查返回堆栈缓冲区的顶部。如果 RSB 查找失败，控制权返回给调度器。这是用于更快函数调用的优化。不支持此优化或没有 RSB 的后端可以选择将其实现为与 ReturnToDispatch 完全相同。

### 终端: If

    SetTerm(IR::Term::If{cond, term_then, term_else})

此终端指令根据 ARM 标志的运行时状态有条件地执行一个终端或另一个终端。
