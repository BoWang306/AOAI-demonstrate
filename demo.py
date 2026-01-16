#!/usr/bin/env python3
"""
Azure OpenAI 模型测试门户 - 演示脚本

此脚本演示如何以编程方式使用 Azure OpenAI API
"""

import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import json

# 加载环境变量
load_dotenv()

def initialize_client():
    """初始化 Azure OpenAI 客户端"""
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    
    if not api_key or not api_base:
        raise ValueError("请设置 AZURE_OPENAI_API_KEY 和 AZURE_OPENAI_ENDPOINT 环境变量")
    
    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=api_base
    )
    
    return client

def demo_chat_completion(client, model="gpt-4.1-nano"):
    """演示基本的聊天完成"""
    print(f"\n{'='*60}")
    print(f"演示 1: 基本聊天完成 (模型: {model})")
    print(f"{'='*60}\n")
    
    messages = [
        {"role": "system", "content": "你是一个有帮助的AI助手。"},
        {"role": "user", "content": "用一句话解释什么是机器学习。"}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=100
    )
    
    print(f"问题: {messages[1]['content']}")
    print(f"\n回答: {response.choices[0].message.content}")
    print(f"\n性能指标:")
    print(f"  - 输入 Tokens: {response.usage.prompt_tokens}")
    print(f"  - 输出 Tokens: {response.usage.completion_tokens}")
    print(f"  - 总计 Tokens: {response.usage.total_tokens}")

def demo_streaming(client, model="gpt-5-nano"):
    """演示流式输出"""
    print(f"\n{'='*60}")
    print(f"演示 2: 流式输出 (模型: {model})")
    print(f"{'='*60}\n")
    
    messages = [
        {"role": "user", "content": "写一首关于人工智能的四行诗。"}
    ]
    
    print("问题: " + messages[0]['content'])
    print("\n回答 (流式): ", end="", flush=True)
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.8,
        max_tokens=200,
        stream=True
    )
    
    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    
    print("\n")

def demo_different_temperatures(client, model="gpt-5"):
    """演示不同温度参数的效果"""
    print(f"\n{'='*60}")
    print(f"演示 3: 不同 Temperature 参数对比 (模型: {model})")
    print(f"{'='*60}\n")
    
    prompt = "用三个词描述春天。"
    temperatures = [0.1, 0.7, 1.2]
    
    for temp in temperatures:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
            max_tokens=50
        )
        
        print(f"Temperature = {temp}:")
        print(f"  回答: {response.choices[0].message.content}")
        print()

def demo_code_generation(client, model="gpt-5.2-codex"):
    """演示代码生成"""
    print(f"\n{'='*60}")
    print(f"演示 4: 代码生成 (模型: {model})")
    print(f"{'='*60}\n")
    
    messages = [
        {"role": "system", "content": "你是一个专业的 Python 程序员。"},
        {"role": "user", "content": "写一个 Python 函数，检查一个字符串是否是回文。"}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
        max_tokens=300
    )
    
    print("任务: " + messages[1]['content'])
    print(f"\n生成的代码:\n{response.choices[0].message.content}")

def demo_multi_turn_conversation(client, model="gpt-5.1-chat"):
    """演示多轮对话"""
    print(f"\n{'='*60}")
    print(f"演示 5: 多轮对话 (模型: {model})")
    print(f"{'='*60}\n")
    
    conversation = [
        {"role": "system", "content": "你是一个友好的助手。"}
    ]
    
    # 第一轮
    conversation.append({"role": "user", "content": "什么是深度学习？"})
    response1 = client.chat.completions.create(
        model=model,
        messages=conversation,
        temperature=0.7,
        max_tokens=150
    )
    
    assistant_reply1 = response1.choices[0].message.content
    conversation.append({"role": "assistant", "content": assistant_reply1})
    
    print("用户: " + conversation[1]['content'])
    print(f"助手: {assistant_reply1}\n")
    
    # 第二轮
    conversation.append({"role": "user", "content": "它和机器学习有什么区别？"})
    response2 = client.chat.completions.create(
        model=model,
        messages=conversation,
        temperature=0.7,
        max_tokens=150
    )
    
    assistant_reply2 = response2.choices[0].message.content
    
    print("用户: " + conversation[3]['content'])
    print(f"助手: {assistant_reply2}\n")

def demo_batch_processing(client, model="gpt-5"):
    """演示批量处理"""
    print(f"\n{'='*60}")
    print(f"演示 6: 批量处理 (模型: {model})")
    print(f"{'='*60}\n")
    
    test_cases = [
        "解释什么是API",
        "Python和JavaScript的主要区别是什么",
        "什么是云计算"
    ]
    
    results = []
    
    for idx, question in enumerate(test_cases, 1):
        print(f"处理问题 {idx}/{len(test_cases)}: {question}")
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": question}],
            temperature=0.5,
            max_tokens=100
        )
        
        answer = response.choices[0].message.content
        results.append({
            "question": question,
            "answer": answer,
            "tokens": response.usage.total_tokens
        })
        
        print(f"  回答: {answer[:80]}...")
        print(f"  Tokens: {response.usage.total_tokens}\n")
    
    # 汇总
    total_tokens = sum(r['tokens'] for r in results)
    print(f"批量处理完成！")
    print(f"  - 总问题数: {len(test_cases)}")
    print(f"  - 总 Tokens: {total_tokens}")
    print(f"  - 平均 Tokens: {total_tokens / len(test_cases):.1f}")

def main():
    """主函数"""
    print("\n" + "="*60)
    print("Azure OpenAI 模型测试门户 - 演示脚本")
    print("="*60)
    
    try:
        # 初始化客户端
        print("\n正在初始化 Azure OpenAI 客户端...")
        client = initialize_client()
        print("✅ 客户端初始化成功！")
        
        # 运行演示
        demos = [
            ("基本聊天完成", lambda: demo_chat_completion(client)),
            ("流式输出", lambda: demo_streaming(client)),
            ("Temperature 参数对比", lambda: demo_different_temperatures(client)),
            ("代码生成", lambda: demo_code_generation(client)),
            ("多轮对话", lambda: demo_multi_turn_conversation(client)),
            ("批量处理", lambda: demo_batch_processing(client)),
        ]
        
        print("\n可用的演示:")
        for idx, (name, _) in enumerate(demos, 1):
            print(f"  {idx}. {name}")
        print(f"  0. 运行所有演示")
        
        choice = input("\n请选择要运行的演示 (0-6): ").strip()
        
        if choice == "0":
            for name, demo_func in demos:
                try:
                    demo_func()
                except Exception as e:
                    print(f"❌ 演示失败: {str(e)}\n")
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            idx = int(choice) - 1
            name, demo_func = demos[idx]
            try:
                demo_func()
            except Exception as e:
                print(f"❌ 演示失败: {str(e)}\n")
        else:
            print("❌ 无效的选择")
            return
        
        print("\n" + "="*60)
        print("演示完成！")
        print("="*60 + "\n")
        
    except ValueError as e:
        print(f"\n❌ 错误: {str(e)}")
        print("\n请确保已设置以下环境变量：")
        print("  - AZURE_OPENAI_API_KEY")
        print("  - AZURE_OPENAI_ENDPOINT")
        print("\n可以通过以下方式设置：")
        print("  1. 创建 .env 文件")
        print("  2. 或直接设置环境变量")
        print("\n示例 .env 文件：")
        print("  AZURE_OPENAI_API_KEY=your_key")
        print("  AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/")
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")

if __name__ == "__main__":
    main()
