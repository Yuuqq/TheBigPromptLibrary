# 编译时加密字符串

> 感谢 [SpecterOps](https://specterops.io/) 对本研究的支持，以及 [Duane](https://twitter.com/subat0mik) 和 [Matt](https://twitter.com/matterpreter) 的校对和编辑！
> 同步发布于 [SpecterOps 博客](https://posts.specterops.io/encrypting-strings-at-compile-time-4141dafe5b41)。

简而言之：_你可以使用[这个头文件](https://gist.github.com/EvanMcBroom/ad683e394f84b623da63c2b95f6fb547)来实现可靠的编译时字符串加密，无需任何额外依赖。_

DRM 软件、安全产品或其他敏感代码库的程序员通常需要最小化二进制输出文件中人类可读字符串的数量。这种最小化的目的是阻止他人对其专有技术进行逆向工程。

为满足此要求而采取的常见方法通常会给开发人员增加额外的维护负担，并且容易出错。本文将介绍这些方法及其缺点，同时也会提出一种针对以下目标的替代解决方案：
- 简约的实现以便于集成到项目中
- 简单的使用设计以避免程序员错误
- 内置随机化以阻止自动化字符串恢复

## 常见方法

通常会构建单独的实用程序来预计算用于源代码的混淆字符串。这些工具会生成必须手动添加到项目并在项目中引用的头文件或其他输出。这些工具的使用可以通过工具链自动化，但它们无法很好地与 IDE 集成，并且随着字符串数量的增加，维护起来很繁琐。它们还倾向于以统一的方式混淆字符串，这种方式很容易以自动化方式识别和逆转。

类似地，通常也会构建实用程序来预计算用于比较的字符串哈希值。最早的例子之一记录在"Win32 Assembly Components"中。<sup>1</sup> 这些工具随着字符串数量的增加也变得繁琐，但现在可以通过编译时哈希字符串完全消除它们，[如之前的文章所述](https://gist.github.com/EvanMcBroom/2a9bed888c2755153a9616aa7ae1f79a)。

最后，一些开发团队试图完全消除字符串的使用。不用说，这对于任何有一定开发人员流动的大型或长期项目来说是不可能维持的标准。

## 替代解决方案

现代 C++ 特性可用于在编译时加密字符串，这可以大大减少开发人员的维护开销。有几个库声称支持这种用例。不幸的是，它们在实践中很少有效。少数有效的库需要 [BOOST](https://www.boost.org/) 库，由于开发限制，这可能不是一个选项。<sup>2</sup> 所以我们将构建自己的！

我们将首先创建一个用于编译时字符串加密的基本函数，稍后可以对其进行改进。下面的 `crypt` 函数将把字符串字面量转换为加密的 blob，`make_string` 宏包装 `crypt` 以确保在编译时正确评估。

```cpp
template<typename T, size_t N>
struct encrypted {
    T data[N];
};

template<size_t N>
constexpr auto crypt(const char(&input)[N]) {
    encrypted<char> blob{};
    for (uint32_t index{ 0 }; index < N; index++) {
        blob.data[index] = input[index] ^ 'A';
    }
    return blob;
}

#define make_string(STRING) ([&] {            \
    constexpr auto _{ crypt(STRING) };        \
    return std::string{ crypt(_.data).data }; \
}())
```

`make_string` 宏还将扩展为单个 lambda 表达式，可用于任何变量赋值和参数传递操作。

```cpp
void main() {
    std::string string1{ make_string("String 1") };
    std::string string2 = make_string("String 2");
    func(make_string("String 3"));
}
```

## 改进解决方案

之前的解决方案易于集成和在项目中使用，但逆向工程师也很容易撤销它。它本质上是一个带有静态密钥的 XOR 密码。一旦识别出密钥，整个程序就可以与之进行 XOR 运算，然后可以使用简单的 `strings` 实用程序恢复原始字符串。

用随机比特流替换静态密钥可以防止这个问题。我们现在将创建一组函数，用于在编译时生成这样的流。由于其实现简单性，我们将使用 Park-Miller 的"乘法线性同余生成器"。<sup>3</sup>

```cpp
constexpr uint32_t modulus() {
    return 0x7fffffff;
}

constexpr uint32_t prng(const uint32_t input) {
    return (input * 48271) % modulus();
}
```

我们还需要一个伪随机值作为 `prng` 的初始输入。诚然，在编译时生成这样的值并不容易，但可以使用标准预定义宏如 `__FILE__` 和 `__LINE__` 来实现。下面的 `seed` 函数可以将这些宏作为输入，并将它们减少为单个伪随机值以与 `prng` 一起使用。

> 注意：这些宏由 ANSI C 标准定义，所有编译器都支持。如果你使用非标准宏作为熵源，结果可能会有所不同。

```cpp
template<size_t N>
constexpr uint32_t seed(const char(&entropy)[N], const uint32_t iv = 0) {
    auto value{ iv };
    for (size_t i{ 0 }; i < N; i++) {
        // 将种子的第一个字节与输入字节进行异或
        value = (value & ((~0) << 8)) | ((value & 0xFF) ^ entropy[i]);
        // 左旋转1字节
        value = value << 8 | value >> ((sizeof(value) * 8) - 8);
    }
    // 种子必须小于模数且为奇数
    while (value > modulus()) value = value >> 1;
    return value << 1 | 1;
}
```

最后需要做的是更新我们原来的 `crypt` 和 `make_string` 函数以使用我们的随机比特流生成器。

```cpp
template<typename T, size_t N>
struct encrypted {
    int seed;
    T data[N];
};

template<size_t N>
constexpr auto crypt(const char(&input)[N], const uint32_t seed = 0) {
    encrypted<char, N> blob{};
    blob.seed = seed;
    for (uint32_t index{ 0 }, stream{ seed }; index < N; index++) {
        blob.data[index] = input[index] ^ stream;
        stream = prng(stream);
    }
    return blob;
}

#define make_string(STRING) ([&] {                               \
    constexpr auto _{ crypt(STRING, seed(__FILE__, __LINE__)) }; \
    return std::string{ crypt(_.data, _.seed).data };            \
}())
```

> 注意：如果你使用 Visual Studio，你需要禁用"编辑并继续"功能；否则，[`__LINE__` 宏将无法在常量表达式中使用](https://developercommunity.visualstudio.com/t/-line-cannot-be-used-as-an-argument-for-constexpr/195665#T-N197532)。

## 事件响应

如果你正在调查可能的恶意可执行文件，它也可能包含以这种方式加密的字符串。提供的代码可以保护字符串免受任何粗略检查，但它们都可以使用 [FLARE 的混淆字符串求解器](https://github.com/mandiant/flare-floss)（FLOSS）恢复。

还可以进行额外的小改进以防止使用 FLOSS 进行自动化字符串恢复。一个例子是在解密例程中包含基于异常的控制流。但是，为了事件响应人员的利益，这些改进将不会呈现，留作读者的练习。

## 结论

我们现在有了一个编译时加密字符串的解决方案，它满足我们所有的原始目标，并且可以与任何主流编译器配合使用。完整源代码可以在[这里](https://gist.github.com/EvanMcBroom/ad683e394f84b623da63c2b95f6fb547)找到。享受吧！:smile:

如果你喜欢阅读这项工作，你可能也会喜欢我的一些旧文章。第一篇涵盖编译时哈希函数，第二篇提供了一种更用户友好的替代方案，用于在位置无关代码中声明字符串的编程习语。

- [使用完整字符串的 Switch 语句](https://gist.github.com/EvanMcBroom/2a9bed888c2755153a9616aa7ae1f79a)
- PIC 和字符串字面量 [第1部分](https://gist.github.com/EvanMcBroom/f5b1bc53977865773802d795ade67273) 和 [第2部分](https://gist.github.com/EvanMcBroom/d7f6a8fe3b4d8f511b132518b9cf80d7)

## 参考文献

1. The Last Stage of Delirium Research Group. _Win32 Assembly Components_, 2002.
`http://www.lsd-pl.net/documents/winasm-1.0.1.pdf`
2. Sebastien Andrivet. _C++11 Metaprogramming Applied to Software Obfuscation_, 2014.
`https://www.blackhat.com/docs/eu-14/materials/eu-14-Andrivet-C-plus-plus11-Metaprogramming-Applied-To-software-Obfuscation-wp.pdf`
3. Stephen Park and Keith Miller. _Random Number Generators_, 1988.
`https://www.firstpr.com.au/dsp/rand31/p1192-park.pdf`
