url

logo

title

description

指令:

GPT instructions:

```markdown
Upon the first user message, call the start method.

This start message returns a user_id. Ensure you pass this user_id to all subsequent requests.
```

GPT Tools/Actions:

```json
"tools": [
  {
    "id": "gzm_cnf_EVq1ynONfvrLAatPz3De4Zaa~gzm_tool_Mma3aW6CnZ7B8ifuMyR6VPwD",
    "type": "plugins_prototype",
    "settings": null,
    "metadata": {
      "action_id": "g-fae716d73ad436e166fe58970d4511d2bd67b8ac",
      "domain": "mapgpt.chatsuite.ai",
      "raw_spec": null,
      "json_schema": {
        "openapi": "3.0.2",
        "servers": [
          {
            "url": "https://mapgpt.chatsuite.ai"
          }
        ],
        "info": {
          "title": "Slow Down and Look Around",
          "description": "A tour guide plugin for ChatGPT that allows you to see what trivia is in your local area",
          "version": "3.0.2",
          "x-logo": {
            "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
          }
        },
        "paths": {
          "/": {
            "get": {
              "summary": "Serve Home",
              "description": "MapGPT website homepage",
              "operationId": "serve_home__get",
              "responses": {
                "200": {
                  "description": "Successful Response",
                  "content": {
                    "text/html": {
                      "schema": {
                        "type": "string"
                      }
                    }
                  }
                }
              }
            }
          },
          "/get_location/{user_id}": {
            "get": {
              "summary": "Get Location",
              "description": "Send user here first to get their location!",
              "operationId": "get_location_get_location__user_id__get",
              "parameters": [
                {
                  "required": true,
                  "schema": {
                    "title": "User Id",
                    "type": "string"
                  },
                  "name": "user_id",
                  "in": "path"
                }
              ],
              "responses": {
                "200": {
                  "description": "Successful Response",
                  "content": {
                    "application/json": {
                      "schema": {}
                    }
                  }
                },
                "422": {
                  "description": "Validation Error",
                  "content": {
                    "application/json": {
                      "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                      }
                    }
                  }
                }
              }
            }
          },
          "/about": {
            "get": {
              "summary": "Serve About",
              "operationId": "serve_about_about_get",
              "responses": {
                "200": {
                  "description": "Successful Response",
                  "content": {
                    "text/html": {
                      "schema": {
                        "type": "string"
                      }
                    }
                  }
                }
              }
            }
          },
          "/privacy": {
            "get": {
              "summary": "Serve Privacy",
              "operationId": "serve_privacy_privacy_get",
              "responses": {
                "200": {
                  "description": "Successful Response",
                  "content": {
                    "text/html": {
                      "schema": {
                        "type": "string"
                      }
                    }
                  }
                }
              }
            }
          },
          "/start": {
            "get": {
              "summary": "Start",
              "operationId": "start_start_get",
              "responses": {
                "200": {
                  "description": "Successful Response",
                  "content": {
                    "application/json": {
                      "schema": {}
                    }
                  }
                }
              }
            }
          },
          "/get_trivia": {
            "get": {
              "tags": [
                "uses-user-id"
              ],
              "summary": "Get Trivia",
              "description": "Uses user ID to 生成 location trivia. This 可以 be retrieved from the unique URL generated (its the last part of the URL).",
              "operationId": "get_trivia_get_trivia_get",
              "parameters": [
                {
                  "required": true,
                  "schema": {
                    "title": "User Id",
                    "type": "string"
                  },
                  "name": "user_id",
                  "in": "query"
                }
              ],
              "responses": {
                "200": {
                  "description": "Successful Response",
                  "content": {
                    "application/json": {
                      "schema": {}
                    }
                  }
                },
                "422": {
                  "description": "Validation Error",
                  "content": {
                    "application/json": {
                      "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                      }
                    }
                  }
                }
              },
              "security": [
                {
                  "HTTPBearer": []
                }
              ]
            }
          },
          "/get_nearby_places/{user_id}": {
            "get": {
              "tags": [
                "uses-user-id"
              ],
              "summary": "Get Nearby Places Fastapi",
              "description": "Uses user ID to 生成 nearby places to visit. This 可以 be retrieved from the unique URL generated (its the last part of the URL).",
              "operationId": "get_nearby_places_fastapi_get_nearby_places__user_id__get",
              "parameters": [
                {
                  "required": true,
                  "schema": {
                    "title": "User Id",
                    "type": "string"
                  },
                  "name": "user_id",
                  "in": "path"
                }
              ],
              "responses": {
                "200": {
                  "description": "Successful Response",
                  "content": {
                    "application/json": {
                      "schema": {}
                    }
                  }
                },
                "422": {
                  "description": "Validation Error",
                  "content": {
                    "application/json": {
                      "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                      }
                    }
                  }
                }
              },
              "security": [
                {
                  "HTTPBearer": []
                }
              ]
            }
          },
          "/google_maps_directions": {
            "get": {
              "tags": [
                "uses-user-id"
              ],
              "summary": "Directions",
              "description": "生成 a google maps url with directions. This 可以 be retrieved from the unique URL generated (its the last part of the URL).",
              "operationId": "directions_google_maps_directions_get",
              "parameters": [
                {
                  "required": true,
                  "schema": {
                    "title": "User Id",
                    "type": "string"
                  },
                  "name": "user_id",
                  "in": "query"
                }
              ],
              "responses": {
                "200": {
                  "description": "Successful Response",
                  "content": {
                    "application/json": {
                      "schema": {}
                    }
                  }
                },
                "422": {
                  "description": "Validation Error",
                  "content": {
                    "application/json": {
                      "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                      }
                    }
                  }
                }
              },
              "security": [
                {
                  "HTTPBearer": []
                }
              ]
            }
          },
          "/.well-known/ai-plugin.json": {
            "get": {
              "summary": "Plugin Manifest",
              "operationId": "plugin_manifest__well_known_ai_plugin_json_get",
              "responses": {
                "200": {
                  "description": "Successful Response",
                  "content": {
                    "application/json": {
                      "schema": {}
                    }
                  }
                }
              }
            }
          }
        },
        "components": {
          "schemas": {
            "HTTPValidationError": {
              "title": "HTTPValidationError",
              "type": "object",
              "properties": {
                "detail": {
                  "title": "Detail",
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/ValidationError"
                  }
                }
              }
            },
            "ValidationError": {
              "title": "ValidationError",
              "required": [
                "loc",
                "msg",
                "type"
              ],
              "type": "object",
              "properties": {
                "loc": {
                  "title": "Location",
                  "type": "array",
                  "items": {
                    "anyOf": [
                      {
                        "type": "string"
                      },
                      {
                        "type": "integer"
                      }
                    ]
                  }
                },
                "msg": {
                  "title": "Message",
                  "type": "string"
                },
                "type": {
                  "title": "Error Type",
                  "type": "string"
                }
              }
            }
          },
          "securitySchemes": {
            "HTTPBearer": {
              "type": "http",
              "scheme": "bearer"
            }
          }
        }
      },
      "auth": {
        "type": "service_http",
        "instructions": "",
        "authorization_type": "bearer",
        "verification_tokens": {},
        "custom_auth_header": ""
      },
      "privacy_policy_url": "https://mapgpt.chatsuite.ai/privacy"
    }
  },
  {
    "id": "gzm_cnf_eOsE56YKzqR8rIKqWvveWinw~gzm_tool_zyGh9Q0l0OI7MfQfTMlvmDkF",
    "type": "browser",
    "settings": null,
    "metadata": null
  },
  {
    "id": "gzm_cnf_eOsE56YKzqR8rIKqWvveWinw~gzm_tool_ybhhiRzPUd47kAex4j3wMh0g",
    "type": "dalle",
    "settings": null,
    "metadata": null
  }
]
```