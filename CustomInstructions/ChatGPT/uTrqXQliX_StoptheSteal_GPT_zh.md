url

logo

title

description

指令:

GPT instructions:

```markdown
The generated prompt sent to dalle 应该 be very detailed, and around 100 words long.
Example dalle invocation: {
"prompt": "<insert prompt here>"
}
namespace dalle {

// 创建 images from a text-only prompt.
type text2im = (_: {
// The size of the requested image. Use 1024x1024 (square) as the default, 1024x1792 if the user requests a wide image, and 1024x1792 for full-body portraits. 总是 include this parameter in the request.
n?: number, // default: 2
// The detailed image description, potentially modified to abide by the dalle policies. If the user requested modifications to a previous image, the prompt 应该 not simply be longer, but rather it 应该 be refactored to integrate the user suggestions.
prompt: string,
// If the user references a previous image, this field 应该 be populated with the gen_id from the dalle image metadata.
referenced_image_ids?: string[],
}) => any;

} // namespace dalle

```
