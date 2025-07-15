import csv
import json
import tkinter as tk
from tkinter import filedialog, messagebox

def convert_csv_to_json(csv_path, json_path, selected_fields):
    scenes = []

    try:
        with open(csv_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                scene = {}
                for field in selected_fields:
                    scene[field] = row.get(field, "")
                scenes.append(scene)

        result = {"scenes": scenes}

        with open(json_path, mode='w', encoding='utf-8') as jsonfile:
            json.dump(result, jsonfile, ensure_ascii=False, indent=2)

        messagebox.showinfo("성공", f"✅ JSON 파일이 저장되었습니다:\n{json_path}")
    except Exception as e:
        messagebox.showerror("오류 발생", f"에러: {str(e)}")


def browse_csv():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")],
        title="CSV 파일 선택"
    )
    csv_entry.delete(0, tk.END)
    csv_entry.insert(0, file_path)

def browse_save_json():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        title="JSON 저장 위치 선택"
    )
    json_entry.delete(0, tk.END)
    json_entry.insert(0, file_path)

def on_convert_click():
    csv_path = csv_entry.get()
    json_path = json_entry.get()
    fields_raw = fields_entry.get()

    if not csv_path or not json_path or not fields_raw.strip():
        messagebox.showwarning("입력 오류", "CSV, JSON, 필드 이름을 모두 입력해주세요.")
        return

    selected_fields = [field.strip() for field in fields_raw.split(",")]
    convert_csv_to_json(csv_path, json_path, selected_fields)

def show_help():
    help_msg = """
[사용법]

1. CSV 파일 선택
2. 저장할 JSON 파일 위치 지정
3. 변환할 필드 이름 입력 (쉼표로 구분)
   예: speaker,text,characterImage,backgroundImage,standingSide,color
4. [변환 실행] 버튼 클릭
"""
    messagebox.showinfo("도움말", help_msg)


# UI 구성
root = tk.Tk()
root.title("CSV → JSON 선택 변환기")
root.geometry("550x320")
root.resizable(False, False)

# CSV 선택
tk.Label(root, text="CSV 파일:").pack(pady=(10, 0))
csv_entry = tk.Entry(root, width=65)
csv_entry.pack()
tk.Button(root, text="CSV 선택", command=browse_csv).pack(pady=3)

# JSON 저장 위치
tk.Label(root, text="JSON 저장 위치:").pack(pady=(10, 0))
json_entry = tk.Entry(root, width=65)
json_entry.pack()
tk.Button(root, text="JSON 저장 위치 선택", command=browse_save_json).pack(pady=3)

# 필드 입력
tk.Label(root, text="추출할 필드 이름 (쉼표 구분):").pack(pady=(10, 0))
fields_entry = tk.Entry(root, width=65)
fields_entry.insert(0, "speaker,text,characterImage,backgroundImage")  # 기본값
fields_entry.pack()

# 버튼들
frame = tk.Frame(root)
frame.pack(pady=15)

tk.Button(frame, text="변환 실행", command=on_convert_click, bg="green", fg="white", width=15).pack(side="left", padx=10)
tk.Button(frame, text="도움말", command=show_help, width=15).pack(side="left", padx=10)

root.mainloop()