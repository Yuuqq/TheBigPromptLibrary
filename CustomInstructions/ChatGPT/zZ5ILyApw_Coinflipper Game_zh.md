# Coinflipper Game（中文译本）

原文：[`zZ5ILyApw_Coinflipper Game.md`](./zZ5ILyApw_Coinflipper Game.md)

```markdown
Coinflipper Game 是一个有参与感的“抛硬币猜面”小游戏。

- 新用户进入时，首先询问用户名与国家（用于通过 API 创建用户档案）。
- 档案创建后，邀请用户在每次抛硬币时选择“正面（heads）”或“反面（tails）”。
- 游戏通过 API 处理每一次猜测，返回结果，并聚焦“当前连胜次数（streak）”。
- 目标是激励用户持续游玩，努力登上全球排行榜（连胜最长者居前）。
- 语气保持友好、支持与鼓励，营造有趣而带竞争感的氛围。
- 游戏现已配备更鲜明的动感 Logo，象征猜测游戏的激情。
```


GPT actions:

```json
{
  "openapi": "3.0.3",
  "info": {
    "title": "Coinflipper API Documentation",
    "description": "An api for guessing coin flips and collect streaks",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://coinflipper-api.matzielab.com"
    }
  ],
  "components": {
    "securitySchemes": {
      "basicAuth": {
        "type": "http",
        "scheme": "Bearer",
        "description": "Basic authentication with api token"
      }
    },
    "schemas": {}
  },
  "paths": {
    "/user/": {
      "post": {
        "parameters": [],
        "responses": {
          "200": {
            "description": "User created successfully. super_secret_user_token is used to identify the user and cant be changed",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "super_secret_user_token": {
                      "type": "string"
                    },
                    "username": {
                      "minLength": 3,
                      "maxLength": 20,
                      "type": "string"
                    },
                    "country": {
                      "minLength": 3,
                      "maxLength": 50,
                      "type": "string"
                    }
                  },
                  "required": [
                    "super_secret_user_token",
                    "username",
                    "country"
                  ]
                }
              },
              "multipart/form-data": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "super_secret_user_token": {
                      "type": "string"
                    },
                    "username": {
                      "minLength": 3,
                      "maxLength": 20,
                      "type": "string"
                    },
                    "country": {
                      "minLength": 3,
                      "maxLength": 50,
                      "type": "string"
                    }
                  },
                  "required": [
                    "super_secret_user_token",
                    "username",
                    "country"
                  ]
                }
              },
              "text/plain": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "super_secret_user_token": {
                      "type": "string"
                    },
                    "username": {
                      "minLength": 3,
                      "maxLength": 20,
                      "type": "string"
                    },
                    "country": {
                      "minLength": 3,
                      "maxLength": 50,
                      "type": "string"
                    }
                  },
                  "required": [
                    "super_secret_user_token",
                    "username",
                    "country"
                  ]
                }
              }
            }
          }
        },
        "operationId": "postUser",
        "summary": "Create a new user by providing a username",
        "description": "Create a new user by providing a username. The returned super_secret_user_token is used to identify the user in the future and should never be shared with anyone.",
        "security": [
          {
            "basicAuth": []
          }
        ],
        "x-openai-isConsequential": false,
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "username": {
                    "minLength": 3,
                    "maxLength": 20,
                    "type": "string"
                  },
                  "country": {
                    "minLength": 3,
                    "maxLength": 50,
                    "type": "string"
                  }
                },
                "required": [
                  "username",
                  "country"
                ],
                "additionalProperties": false
              }
            },
            "multipart/form-data": {
              "schema": {
                "type": "object",
                "properties": {
                  "username": {
                    "minLength": 3,
                    "maxLength": 20,
                    "type": "string"
                  },
                  "country": {
                    "minLength": 3,
                    "maxLength": 50,
                    "type": "string"
                  }
                },
                "required": [
                  "username",
                  "country"
                ],
                "additionalProperties": false
              }
            },
            "text/plain": {
              "schema": {
                "type": "object",
                "properties": {
                  "username": {
                    "minLength": 3,
                    "maxLength": 20,
                    "type": "string"
                  },
                  "country": {
                    "minLength": 3,
                    "maxLength": 50,
                    "type": "string"
                  }
                },
                "required": [
                  "username",
                  "country"
                ],
                "additionalProperties": false
              }
            }
          }
        }
      },
      "put": {
        "parameters": [],
        "responses": {
          "200": {
            "description": "Username updated successfully",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "user_updated": {
                      "type": "boolean"
                    },
                    "username": {
                      "minLength": 3,
                      "maxLength": 20,
                      "type": "string"
                    },
                    "country": {
                      "minLength": 3,
                      "maxLength": 50,
                      "type": "string"
                    }
                  },
                  "required": [
                    "user_updated",
                    "username",
                    "country"
                  ]
                }
              },
              "multipart/form-data": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "user_updated": {
                      "type": "boolean"
                    },
                    "username": {
                      "minLength": 3,
                      "maxLength": 20,
                      "type": "string"
                    },
                    "country": {
                      "minLength": 3,
                      "maxLength": 50,
                      "type": "string"
                    }
                  },
                  "required": [
                    "user_updated",
                    "username",
                    "country"
                  ]
                }
              },
              "text/plain": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "user_updated": {
                      "type": "boolean"
                    },
                    "username": {
                      "minLength": 3,
                      "maxLength": 20,
                      "type": "string"
                    },
                    "country": {
                      "minLength": 3,
                      "maxLength": 50,
                      "type": "string"
                    }
                  },
                  "required": [
                    "user_updated",
                    "username",
                    "country"
                  ]
                }
              }
            }
          },
          "404": {
            "description": "User doesnt exist",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "user_updated": {
                      "type": "boolean"
                    },
                    "error": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "user_updated",
                    "error"
                  ]
                }
              },
              "multipart/form-data": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "user_updated": {
                      "type": "boolean"
                    },
                    "error": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "user_updated",
                    "error"
                  ]
                }
              },
              "text/plain": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "user_updated": {
                      "type": "boolean"
                    },
                    "error": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "user_updated",
                    "error"
                  ]
                }
              }
            }
          }
        },
        "operationId": "putUser",
        "summary": "Update username and country",
        "description": "Update username by providing the super_secret_user_token and the new username and country",
        "security": [
          {
            "basicAuth": []
          }
        ],
        "x-openai-isConsequential": false,
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "username": {
                    "minLength": 3,
                    "maxLength": 20,
                    "type": "string"
                  },
                  "country": {
                    "minLength": 3,
                    "maxLength": 50,
                    "type": "string"
                  },
                  "super_secret_user_token": {
                    "type": "string"
                  }
                },
                "required": [
                  "username",
                  "country",
                  "super_secret_user_token"
                ],
                "additionalProperties": false
              }
            },
            "multipart/form-data": {
              "schema": {
                "type": "object",
                "properties": {
                  "username": {
                    "minLength": 3,
                    "maxLength": 20,
                    "type": "string"
                  },
                  "country": {
                    "minLength": 3,
                    "maxLength": 50,
                    "type": "string"
                  },
                  "super_secret_user_token": {
                    "type": "string"
                  }
                },
                "required": [
                  "username",
                  "country",
                  "super_secret_user_token"
                ],
                "additionalProperties": false
              }
            },
            "text/plain": {
              "schema": {
                "type": "object",
                "properties": {
                  "username": {
                    "minLength": 3,
                    "maxLength": 20,
                    "type": "string"
                  },
                  "country": {
                    "minLength": 3,
                    "maxLength": 50,
                    "type": "string"
                  },
                  "super_secret_user_token": {
                    "type": "string"
                  }
                },
                "required": [
                  "username",
                  "country",
                  "super_secret_user_token"
                ],
                "additionalProperties": false
              }
            }
          }
        }
      }
    },
    "/flip-coin/": {
      "post": {
        "parameters": [],
        "responses": {
          "200": {
            "description": "The result of the coin flip and whether the user guessed correctly or not as well ass current streak or if it was lost",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "result": {
                      "type": "string"
                    },
                    "guessed_correctly": {
                      "type": "boolean"
                    },
                    "current_streak": {
                      "type": "number"
                    },
                    "lost_streak": {
                      "type": "boolean"
                    },
                    "streak_was": {
                      "type": "number"
                    }
                  }
                }
              },
              "multipart/form-data": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "result": {
                      "type": "string"
                    },
                    "guessed_correctly": {
                      "type": "boolean"
                    },
                    "current_streak": {
                      "type": "number"
                    },
                    "lost_streak": {
                      "type": "boolean"
                    },
                    "streak_was": {
                      "type": "number"
                    }
                  }
                }
              },
              "text/plain": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "result": {
                      "type": "string"
                    },
                    "guessed_correctly": {
                      "type": "boolean"
                    },
                    "current_streak": {
                      "type": "number"
                    },
                    "lost_streak": {
                      "type": "boolean"
                    },
                    "streak_was": {
                      "type": "number"
                    }
                  }
                }
              }
            }
          }
        },
        "operationId": "postFlip-coin",
        "summary": "Flip a coin with a guess",
        "description": "Flip a coin with a guess. The super_secret_user_token is used to identify the user guessing.",
        "security": [
          {
            "basicAuth": []
          }
        ],
        "x-openai-isConsequential": false,
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "super_secret_user_token": {
                    "type": "string"
                  },
                  "guessed_heads": {
                    "type": "boolean"
                  }
                },
                "required": [
                  "super_secret_user_token",
                  "guessed_heads"
                ],
                "additionalProperties": false
              }
            },
            "multipart/form-data": {
              "schema": {
                "type": "object",
                "properties": {
                  "super_secret_user_token": {
                    "type": "string"
                  },
                  "guessed_heads": {
                    "type": "boolean"
                  }
                },
                "required": [
                  "super_secret_user_token",
                  "guessed_heads"
                ],
                "additionalProperties": false
              }
            },
            "text/plain": {
              "schema": {
                "type": "object",
                "properties": {
                  "super_secret_user_token": {
                    "type": "string"
                  },
                  "guessed_heads": {
                    "type": "boolean"
                  }
                },
                "required": [
                  "super_secret_user_token",
                  "guessed_heads"
                ],
                "additionalProperties": false
              }
            }
          }
        }
      }
    },
    "/streak/all/self": {
      "get": {
        "parameters": [
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "userId",
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "All streaks for a user",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "all_streaks": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "streak_length": {
                            "type": "number"
                          },
                          "has_ended": {
                            "type": "boolean"
                          },
                          "created_at": {
                            "type": "string"
                          },
                          "updated_at": {
                            "type": "string"
                          }
                        },
                        "required": [
                          "streak_length",
                          "has_ended",
                          "created_at",
                          "updated_at"
                        ]
                      }
                    }
                  },
                  "required": [
                    "all_streaks"
                  ]
                }
              },
              "multipart/form-data": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "all_streaks": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "streak_length": {
                            "type": "number"
                          },
                          "has_ended": {
                            "type": "boolean"
                          },
                          "created_at": {
                            "type": "string"
                          },
                          "updated_at": {
                            "type": "string"
                          }
                        },
                        "required": [
                          "streak_length",
                          "has_ended",
                          "created_at",
                          "updated_at"
                        ]
                      }
                    }
                  },
                  "required": [
                    "all_streaks"
                  ]
                }
              },
              "text/plain": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "all_streaks": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "streak_length": {
                            "type": "number"
                          },
                          "has_ended": {
                            "type": "boolean"
                          },
                          "created_at": {
                            "type": "string"
                          },
                          "updated_at": {
                            "type": "string"
                          }
                        },
                        "required": [
                          "streak_length",
                          "has_ended",
                          "created_at",
                          "updated_at"
                        ]
                      }
                    }
                  },
                  "required": [
                    "all_streaks"
                  ]
                }
              }
            }
          },
          "404": {
            "description": "No streaks found",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "no_streaks": {
                      "type": "boolean"
                    }
                  },
                  "required": [
                    "no_streaks"
                  ]
                }
              },
              "multipart/form-data": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "no_streaks": {
                      "type": "boolean"
                    }
                  },
                  "required": [
                    "no_streaks"
                  ]
                }
              },
              "text/plain": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "no_streaks": {
                      "type": "boolean"
                    }
                  },
                  "required": [
                    "no_streaks"
                  ]
                }
              }
            }
          }
        },
        "operationId": "getStreakAllSelf",
        "summary": "Get all streaks for a user",
        "description": "Get all streaks for a user. The streaks are sorted by the streak length, with the longest streak first.",
        "security": [
          {
            "basicAuth": []
          }
        ],
        "x-openai-isConsequential": false
      }
    },
    "/streak/current_streak/self": {
      "get": {
        "parameters": [
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "userId",
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "The current streak",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "current_streak": {
                      "type": "number"
                    }
                  },
                  "required": [
                    "current_streak"
                  ]
                }
              },
              "multipart/form-data": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "current_streak": {
                      "type": "number"
                    }
                  },
                  "required": [
                    "current_streak"
                  ]
                }
              },
              "text/plain": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "current_streak": {
                      "type": "number"
                    }
                  },
                  "required": [
                    "current_streak"
                  ]
                }
              }
            }
          }
        },
        "operationId": "getStreakCurrent_streakSelf",
        "summary": "Get current streak for a user",
        "description": "Get current streak for a user. If the user has no streaks, the current streak is 0.",
        "security": [
          {
            "basicAuth": []
          }
        ],
        "x-openai-isConsequential": false
      }
    },
    "/streak/longest_streak/self": {
      "get": {
        "parameters": [
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "userId",
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "The longest streak",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "longest_streak": {
                      "type": "number"
                    }
                  },
                  "required": [
                    "longest_streak"
                  ]
                }
              },
              "multipart/form-data": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "longest_streak": {
                      "type": "number"
                    }
                  },
                  "required": [
                    "longest_streak"
                  ]
                }
              },
              "text/plain": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "longest_streak": {
                      "type": "number"
                    }
                  },
                  "required": [
                    "longest_streak"
                  ]
                }
              }
            }
          }
        },
        "operationId": "getStreakLongest_streakSelf",
        "summary": "Get longest streak for a user",
        "description": "Get longest streak for a user. If the user has no streaks, the longest streak is 0.",
        "security": [
          {
            "basicAuth": []
          }
        ],
        "x-openai-isConsequential": false
      }
    },
    "/streak/toplist": {
      "get": {
        "parameters": [
          {
            "schema": {
              "type": "string"
            },
            "in": "query",
            "name": "userId",
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "The top 20 longest streaks",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "longest_streaks": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "streak_count": {
                            "type": "number"
                          },
                          "username": {
                            "type": "string"
                          },
                          "country": {
                            "anyOf": [
                              {
                                "type": "null"
                              },
                              {
                                "type": "string"
                              }
                            ]
                          },
                          "is_current_user": {
                            "type": "boolean"
                          },
                          "is_ongoing": {
                            "type": "boolean"
                          },
                          "created_at": {
                            "type": "string"
                          },
                          "updated_at": {
                            "type": "string"
                          }
                        },
                        "required": [
                          "streak_count",
                          "username",
                          "country",
                          "is_current_user",
                          "is_ongoing",
                          "created_at",
                          "updated_at"
                        ]
                      }
                    }
                  },
                  "required": [
                    "longest_streaks"
                  ]
                }
              },
              "multipart/form-data": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "longest_streaks": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "streak_count": {
                            "type": "number"
                          },
                          "username": {
                            "type": "string"
                          },
                          "country": {
                            "anyOf": [
                              {
                                "type": "null"
                              },
                              {
                                "type": "string"
                              }
                            ]
                          },
                          "is_current_user": {
                            "type": "boolean"
                          },
                          "is_ongoing": {
                            "type": "boolean"
                          },
                          "created_at": {
                            "type": "string"
                          },
                          "updated_at": {
                            "type": "string"
                          }
                        },
                        "required": [
                          "streak_count",
                          "username",
                          "country",
                          "is_current_user",
                          "is_ongoing",
                          "created_at",
                          "updated_at"
                        ]
                      }
                    }
                  },
                  "required": [
                    "longest_streaks"
                  ]
                }
              },
              "text/plain": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "longest_streaks": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "streak_count": {
                            "type": "number"
                          },
                          "username": {
                            "type": "string"
                          },
                          "country": {
                            "anyOf": [
                              {
                                "type": "null"
                              },
                              {
                                "type": "string"
                              }
                            ]
                          },
                          "is_current_user": {
                            "type": "boolean"
                          },
                          "is_ongoing": {
                            "type": "boolean"
                          },
                          "created_at": {
                            "type": "string"
                          },
                          "updated_at": {
                            "type": "string"
                          }
                        },
                        "required": [
                          "streak_count",
                          "username",
                          "country",
                          "is_current_user",
                          "is_ongoing",
                          "created_at",
                          "updated_at"
                        ]
                      }
                    }
                  },
                  "required": [
                    "longest_streaks"
                  ]
                }
              }
            }
          },
          "404": {
            "description": "No toplist found",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "no_toplist": {
                      "type": "boolean"
                    }
                  },
                  "required": [
                    "no_toplist"
                  ]
                }
              },
              "multipart/form-data": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "no_toplist": {
                      "type": "boolean"
                    }
                  },
                  "required": [
                    "no_toplist"
                  ]
                }
              },
              "text/plain": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "no_toplist": {
                      "type": "boolean"
                    }
                  },
                  "required": [
                    "no_toplist"
                  ]
                }
              }
            }
          }
        },
        "operationId": "getStreakToplist",
        "summary": "Get top 20 longest streaks",
        "description": "Get top 20 longest streaks. The streaks are sorted by the streak length, with the longest streak first.",
        "security": [
          {
            "basicAuth": []
          }
        ],
        "x-openai-isConsequential": false
      }
    }
  }
}
```