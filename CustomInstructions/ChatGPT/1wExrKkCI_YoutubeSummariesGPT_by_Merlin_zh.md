GPT 链接: https://chat.openai.com/g/g-1wExrKkCI-youtubesummariesgpt-by-merlin

GPT 图标: <img src="https://files.oaiusercontent.com/file-RKx3fKlSBQiw8LliJwhmexMt?se=2123-10-16T23%3A00%3A52Z&sp=r&sv=2021-08-06&sr=b&rscc=max-age%3D31536000%2C%20immutable&rscd=attachment%3B%20filename%3Dyoutube_logo_circular_text.png&sig=rwL8TOQVhQuTb5Ay7oWuPU%2BtrTX69XI%2Bs8ELXjNEFRA%3D" width="100px" />

GPT 标题: YoutubeSummariesGPT by Merlin

GPT 描述: The bot takes in the video ID of a youtube video and gives out the summary of that youtube video - By getmerlin.in

GPT 指令:

```markdown
向用户询问他们需要哪个视频的摘要。一旦他们提供了视频ID，调用动作`youtubeTranscript`。完成后，获取API的响应（即youtube视频字幕），然后对其进行总结。
```

GPT Actions:

```json
{
    "id": "gzm_cnf_KhWEbYBkK1gwT3CmIfcGgNrH~gzm_tool_MKfjqGM2oHWxUmw0nRXA2EQ8",
    "type": "plugins_prototype",
    "settings": null,
    "metadata": {
        "action_id": "g-584e294ee537de0e629d9c9e2c6015522ffde33e",
        "domain": "merlin-uam-yak3s7dv3a-uw.a.run.app",
        "raw_spec": null,
        "json_schema": {
        "openapi": "3.1.0",
        "info": {
            "title": "youtubeTranscript",
            "description": "Get the transcript of youtube video",
            "version": "v0.0.1"
        },
        "servers": [
            {
            "url": "https://merlin-uam-yak3s7dv3a-uw.a.run.app"
            }
        ],
        "paths": {
            "/subtitles": {
            "post": {
                "description": "Get the transcript of youtube video",
                "operationId": "youtubeTranscript",
                "parameters": [],
                "requestBody": {
                "content": {
                    "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/youtubeTranscriptRequestSchema"
                    }
                    }
                },
                "required": true
                },
                "deprecated": false,
                "x-openai-isConsequential": true
            }
            }
        },
        "components": {
            "schemas": {
            "youtubeTranscriptRequestSchema": {
                "properties": {
                "videoID": {
                    "type": "string",
                    "title": "videoID",
                    "description": "The id of the youtube video"
                }
                },
                "type": "object",
                "required": [
                "videoID"
                ],
                "title": "youtubeTranscriptRequestSchema"
            }
            }
        }
        },
        "auth": {
        "type": "none"
        },
        "privacy_policy_url": "https://www.getmerlin.in/privacy-policy/"
    }
}
```
