# 寄存器分配（x64 后端）

`HostLoc` 包含值。`HostLoc`（"主机值位置"）是主机 CPU 寄存器或主机溢出位置。

值一旦设置就无法更改。但是值可以由寄存器分配器在 `HostLoc` 之间移动。这由寄存器分配器本身处理，使用寄存器分配器的代码不需要也不应该在寄存器之间移动值。

寄存器分配器基于三个概念：`Use`、`Def` 和 `Scratch`。

* `Use`：使用一个值。
* `Define`：定义一个值，这是唯一设置值的时机。
* `Scratch`：分配一个可以随意修改的寄存器。

注意 `Use` 一个值会将其 `use_count` 减一。当 `use_count` 达到零时，该值被丢弃且不再存在。

`RegAlloc` 上的成员函数只是上述概念的组合。

### `Scratch`

    Xbyak::Reg64 ScratchGpr(HostLocList desired_locations = any_gpr)
    Xbyak::Xmm ScratchXmm(HostLocList desired_locations = any_xmm)

在运行时，分配 `desired_locations` 中的一个寄存器。你可以自由修改该寄存器。该寄存器在分配作用域结束时被丢弃。

### 纯 `Use`

    Xbyak::Reg64 UseGpr(Argument& arg);
    Xbyak::Xmm UseXmm(Argument& arg);
    OpArg UseOpArg(Argument& arg);
    void Use(Argument& arg, HostLoc host_loc);

在运行时，对应于 `arg` 的值将被放置在寄存器中。实际的寄存器由调用上述哪个函数决定。`UseGpr` 将其放在未使用的 GPR 中，`UseXmm` 将其放在未使用的 XMM 寄存器中，`UseOpArg` 可能在寄存器中也可能在内存位置中，`Use` 允许你指定要使用的特定寄存器（GPR 或 XMM）。

此寄存器**必须不**更改其值。

### `UseScratch`

    Xbyak::Reg64 UseScratchGpr(Argument& arg);
    Xbyak::Xmm UseScratchXmm(Argument& arg);
    void UseScratch(Argument& arg, HostLoc host_loc);

在运行时，对应于 `arg` 的值将被放置在寄存器中。实际的寄存器由调用上述哪个函数决定。`UseScratchGpr` 将其放在未使用的 GPR 中，`UseScratchXmm` 将其放在未使用的 XMM 寄存器中，`UseScratch` 允许你指定要使用的特定寄存器（GPR 或 XMM）。

返回值是分配给你的寄存器。

你可以自由修改寄存器中的值。该寄存器在分配作用域结束时被丢弃。

### `Define` 为寄存器

`Define` 是值的定义。这是唯一可以设置值的时机。

    void DefineValue(IR::Inst* inst, const Xbyak::Reg& reg);

通过调用 `DefineValue`，你声明你希望为 `inst` 定义值，并且你已将值写入指定的寄存器 `reg`。

### `Define` 为另一个值的别名

向现有值添加 `Define`。

    void DefineValue(IR::Inst* inst, Argument& arg);

你声明 `inst` 的值与 `arg` 的值相同。不会发出主机机器指令。

## 何时使用每种方法？

* 尽可能优先使用 `Use` 而不是 `UseScratch`。
* 尽可能优先使用 `OpArg` 变体。
* 尽可能优先**不**使用特定的 `HostLoc` 变体。
