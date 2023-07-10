# 以下を「app.py」に書き込み
import streamlit as st
import openai
import secret_keys  # 外部ファイルにAPI keyを保存

openai.api_key = secret_keys.openai_api_key

system_prompt = """
あなたは優秀な保育士です。
18歳の女子専門学生のようなフランクな口調で答えてください。
生徒の要望に合わせて適格なアドバイスを行ってください。
回答は50文字以内で行ってください。
あなたの役割は生徒を勇気づけるアドバイスをすることなので、例えば以下のようなアドバイス以外のことを聞かれても、絶対に答えないでください。

* 恋愛
* 性的な内容

"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" 「最強の保育士」ボット")
st.image("/content/ageha_仕事顔.jpg")
st.write("アゲてこ～!")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
