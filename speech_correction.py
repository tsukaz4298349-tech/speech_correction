import speech_recognition as sr
import re

def tamego_to_teineigo(text):
    """タメ口を丁寧語に変換する関数"""

    #変換パターン
    patterns = {
        r"だね$": "ですね", #Raw文字列記法
        r"こんにちは": "ごきげんよう",
        r"(だ|だぜ|だよ)$": "です",
        r"^よう": "やあ", #キャレット記号
        r"しようぜ$": "しましょう",
        r"いいね": "いいですね",
        r"(飯|家族|注意)": r"ご\1",
        r"(茶|店|祭り)": r"お\1",
        r"(お前|あんた|お主|貴様)": "あなた",
        r"(僕|俺|あたし|拙者|吾輩)": "私",
        r"いいよ": "いいですよ",
        r"ありがとう": "ありがとうございます",
        r"いやいや": "いいえ",
        r"できるか": "できますか",
        r"だっけ": "でしょうか",
        r"行かないか": "行きませんか",
        r"行くか": "行きましょうか",
        r"しよう": "しましょう",
        }
    
    #ひらがなの重複削除を行わないワードリスト
    no_remove_hiragana = ["いいですね", "いいえ", "いいですよ"]
    
    #テキストをスペースで分離する
    sentences = text.split(" ")

    #変換
    teineigo_sentences = []
    dummy_mapping = []
    for sentence in sentences:
        for pattern, replacement in patterns.items():
            sentence = re.sub(pattern, replacement, sentence) #テキスト変換

            #重複削除を行わない文字列はダミー文字列に置き換える
            for no_remove in no_remove_hiragana:
                if no_remove in sentence:
                    dummy_text = "X" * len(no_remove)
                    dummy_mapping.append((dummy_text, no_remove))
                    sentence = sentence.replace(no_remove, dummy_text)

            #ひらがなの重複削除を行う
            sentence = re.sub(r"([ぁ-ん])\1+", r"\1", sentence)

            #ダミー文字列を元に戻す
            for dummy_text, orizinal_text in dummy_mapping:
                sentence = sentence.replace(dummy_text, orizinal_text)

        teineigo_sentences.append(sentence)

    joined_text = " ".join(teineigo_sentences) #1つの文章に結合
        

    return joined_text

#音声の録音
r = sr.Recognizer() #音声認識機能

#繰り返し処理
is_first_time = True
while True:
    with sr.Microphone() as source:
        if is_first_time:
            r.adjust_for_ambient_noise(source, duration=1) #環境音を測定する
            is_first_time = False
        print("マイクに向かってタメ口で話しかけてください")
        audio = r.listen(source) #音声を録音する

    try:
        recognized_text = r.recognize_google(audio, language = 'ja')
        print(f"音声認識結果「{recognized_text}」")
        teinei_text = tamego_to_teineigo(recognized_text)
        print(f"丁寧語変換結果「{teinei_text}」")

        if"プログラム終了" in teinei_text:
            break

    except sr.UnknownValueError: #不明な値エラー
        print("認識できませんでした。")
    except sr.RequestError as e: #ネットワークエラー
        print("ネットワークエラーが発生しました。")
