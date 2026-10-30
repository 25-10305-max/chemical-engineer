"""
[화학공학 GUI 게임] 스마트 반응기 열폭주 방어 및 최적 수율 달성 게임
- Tkinter 기반 (파이썬 기본 내장, 추가 설치 불필요)
- 게이지 바, 애니메이션 반응기 색상 변화, 직관적인 제어 버튼 탑재
"""

import tkinter as tk
from tkinter import ttk, messagebox

class ReactorGame:
    def __init__(self, root):
        self.root = root
        self.root.title("화학공학 시뮬레이션: 스마트 반응기 제어 챌린지")
        self.root.geometry("640x720")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6f9")

        # 공정 변수 초기화
        self.reset_game_state()

        # UI 구성
        self.create_widgets()
        self.update_ui()

    def reset_game_state(self):
        self.temp = 45.0          # 현재 온도 (℃)
        self.yield_rate = 0.0     # 수율 (%)
        self.turn = 1             # 현재 턴
        self.max_turns = 10       # 총 턴 수
        self.game_over = False
        self.log_messages = [
            "공정이 시작되었습니다.",
            "목표: 10턴 내에 열폭주(100℃ 초과)를 막고 수율 90% 이상을 달성하세요!"
        ]

    def create_widgets(self):
        # 상단 헤더
        header_frame = tk.Frame(self.root, bg="#2c3e50", pady=15)
        header_frame.pack(fill="x")
        
        title_label = tk.Label(
            header_frame, 
            text="⚗️ 화학공정 엔지니어: CSTR 반응기 제어", 
            font=("맑은 고딕", 16, "bold"), 
            fg="white", 
            bg="#2c3e50"
        )
        title_label.pack()
        
        sub_label = tk.Label(
            header_frame, 
            text="화학II 반응속도론 & 발열반응 열폭주(Thermal Runaway) 방어", 
            font=("맑은 고딕", 10), 
            fg="#bdc3c7", 
            bg="#2c3e50"
        )
        sub_label.pack(pady=2)

        # 상태 대시보드 프레임
        status_frame = tk.LabelFrame(
            self.root, 
            text=" 공정 실시간 모니터링 대시보드 ", 
            font=("맑은 고딕", 11, "bold"),
            bg="white", 
            padx=15, 
            pady=15
        )
        status_frame.pack(fill="x", padx=20, pady=12)

        # 턴 표시
        self.turn_label = tk.Label(
            status_frame, 
            text=f"운전 진행: 턴 {self.turn} / {self.max_turns}", 
            font=("맑은 고딕", 12, "bold"), 
            bg="white", 
            fg="#34495e"
        )
        self.turn_label.pack(anchor="w", pady=2)

        # 온도 모니터링 & 프로그레스바
        temp_title_frame = tk.Frame(status_frame, bg="white")
        temp_title_frame.pack(fill="x", pady=(8, 2))
        
        tk.Label(temp_title_frame, text="🌡️ 반응기 내부 온도", font=("맑은 고딕", 10, "bold"), bg="white").pack(side="left")
        self.temp_val_label = tk.Label(temp_title_frame, text=f"{self.temp:.1f} ℃", font=("맑은 고딕", 11, "bold"), bg="white", fg="#e74c3c")
        self.temp_val_label.pack(side="right")

        self.temp_bar = ttk.Progressbar(status_frame, maximum=100, length=560)
        self.temp_bar.pack(fill="x", pady=4)

        # 수율 모니터링 & 프로그레스바
        yield_title_frame = tk.Frame(status_frame, bg="white")
        yield_title_frame.pack(fill="x", pady=(10, 2))

        tk.Label(yield_title_frame, text="📈 생성물 반응 수율 (목표 90% 이상)", font=("맑은 고딕", 10, "bold"), bg="white").pack(side="left")
        self.yield_val_label = tk.Label(yield_title_frame, text=f"{self.yield_rate:.1f} %", font=("맑은 고딕", 11, "bold"), bg="white", fg="#2980b9")
        self.yield_val_label.pack(side="right")

        self.yield_bar = ttk.Progressbar(status_frame, maximum=100, length=560)
        self.yield_bar.pack(fill="x", pady=4)

        # 안전 경고 배너
        self.warning_label = tk.Label(
            status_frame, 
            text="✅ 정상 상태: 적정 온도 범위에서 안정적으로 반응 중입니다.", 
            font=("맑은 고딕", 10, "bold"), 
            bg="#e8f8f5", 
            fg="#16a085", 
            pady=6
        )
        self.warning_label.pack(fill="x", pady=(10, 0))

        # 조작 버튼 프레임
        control_frame = tk.LabelFrame(
            self.root, 
            text=" 공정 제어 밸브 및 조작 장치 ", 
            font=("맑은 고딕", 11, "bold"),
            bg="white", 
            padx=15, 
            pady=12
        )
        control_frame.pack(fill="x", padx=20, pady=5)

        btn_grid = tk.Frame(control_frame, bg="white")
        btn_grid.pack(fill="x")

        # 조작 버튼 4종 (2x2 그리드)
        btn1 = tk.Button(
            btn_grid, text="❄️ [강력 냉각]\n냉각수 최대 공급 (-18℃)", 
            font=("맑은 고딕", 10), bg="#d6eaf8", activebackground="#aed6f1",
            relief="groove", height=2, command=lambda: self.execute_turn(1)
        )
        btn1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        btn2 = tk.Button(
            btn_grid, text="💧 [정상 냉각]\n냉각수 적정 유지 (-9℃)", 
            font=("맑은 고딕", 10), bg="#ebf5fb", activebackground="#d4e6f1",
            relief="groove", height=2, command=lambda: self.execute_turn(2)
        )
        btn2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        btn3 = tk.Button(
            btn_grid, text="🌪️ [교반 가속]\n모터 회전 증가 (+5℃)", 
            font=("맑은 고딕", 10), bg="#fef9e7", activebackground="#fdebd0",
            relief="groove", height=2, command=lambda: self.execute_turn(3)
        )
        btn3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        btn4 = tk.Button(
            btn_grid, text="🧪 [촉매 투입]\n반응 활성화 촉진 (+18℃)", 
            font=("맑은 고딕", 10), bg="#fbeee6", activebackground="#f5cba7",
            relief="groove", height=2, command=lambda: self.execute_turn(4)
        )
        btn4.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        btn_grid.columnconfigure(0, weight=1)
        btn_grid.columnconfigure(1, weight=1)

        # 운전 로그창 (텍스트 창)
        log_frame = tk.LabelFrame(
            self.root, 
            text=" 공정 운전 일지 (Log) ", 
            font=("맑은 고딕", 10),
            bg="white", 
            padx=10, 
            pady=5
        )
        log_frame.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        self.log_text = tk.Text(log_frame, height=6, font=("Consolas", 9), state="disabled", bg="#fafafa", relief="flat")
        self.log_text.pack(fill="both", expand=True)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"> {message}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def execute_turn(self, choice):
        if self.game_over:
            return

        # 발열 반응 특성 (기본적으로 매 턴 +8℃ 발열)
        exotherm = 8.0

        if choice == 1:
            delta_t = exotherm - 18.0
            added_yield = max(1.0, (self.temp / 25.0) * 3.0)
            act_name = "강력 냉각"
        elif choice == 2:
            delta_t = exotherm - 9.0
            added_yield = max(2.0, (self.temp / 20.0) * 5.0)
            act_name = "정상 냉각"
        elif choice == 3:
            delta_t = exotherm + 5.0
            added_yield = max(3.0, (self.temp / 18.0) * 7.5)
            act_name = "교반 가속"
        elif choice == 4:
            delta_t = exotherm + 18.0
            added_yield = max(5.0, (self.temp / 15.0) * 11.5)
            act_name = "촉매 투입"

        self.temp += delta_t
        self.yield_rate += added_yield

        if self.yield_rate > 100.0:
            self.yield_rate = 100.0

        self.log(f"[턴 {self.turn}] {act_name} 실행 -> 온도 {self.temp:.1f}℃ ({delta_t:+.1f}℃), 수율 {self.yield_rate:.1f}% (+{added_yield:.1f}%)")
        self.turn += 1

        self.update_ui()
        self.check_game_conditions()

    def update_ui(self):
        # 게이지 및 라벨 갱신
        self.turn_label.config(text=f"운전 진행: 턴 {min(self.turn, self.max_turns)} / {self.max_turns}")
        self.temp_val_label.config(text=f"{self.temp:.1f} ℃")
        self.yield_val_label.config(text=f"{self.yield_rate:.1f} %")

        self.temp_bar['value'] = min(max(self.temp, 0), 100)
        self.yield_bar['value'] = self.yield_rate

        # 위험도별 경고 표시
        if self.temp >= 85:
            self.warning_label.config(
                text="🚨 [위험] 온도가 너무 높습니다! 열폭주(100℃) 폭발 직전!",
                bg="#fdebd0", fg="#c0392b"
            )
        elif self.temp <= 35:
            self.warning_label.config(
                text="⚠️ [경고] 저온 상태! 반응 활성화 에너지가 부족해 반응이 정지됩니다.",
                bg="#ebf5fb", fg="#2980b9"
            )
        else:
            self.warning_label.config(
                text="✅ 정상 상태: 적정 온도 범위에서 고효율 반응 진행 중.",
                bg="#e8f8f5", fg="#16a085"
            )

    def check_game_conditions(self):
        # 1. 열폭주 폭발 (온도 100도 초과)
        if self.temp > 100.0:
            self.game_over = True
            messagebox.showerror(
                "💥 열폭주(Thermal Runaway) 발생!",
                f"온도가 {self.temp:.1f}℃로 100℃를 초과하여 반응기가 폭발했습니다!\n\n"
                f"화학공학 교훈: 발열 반응에서 열 제거 속도가 열 발생 속도를\n"
                f"따라가지 못하면 폭발적인 연쇄 온도 상승이 발생합니다.\n\n"
                f"최종 도달 수율: {self.yield_rate:.1f}%"
            )
            self.prompt_restart()
            return

        # 2. 반응기 동결 (온도 30도 미만)
        if self.temp < 30.0:
            self.game_over = True
            messagebox.showwarning(
                "❄️ 반응 정지 (동결)",
                f"온도가 {self.temp:.1f}℃로 떨어져 반응이 멈췄습니다.\n\n"
                f"화학II 개념: 온도가 너무 낮으면 활성화 에너지 이상의 분자 수가 급감하여\n"
                f"유효 충돌 빈도가 떨어져 반응이 진행되지 않습니다.\n\n"
                f"최종 도달 수율: {self.yield_rate:.1f}%"
            )
            self.prompt_restart()
            return

        # 3. 조기 100% 달성 또는 10턴 종료 판정
        if self.yield_rate >= 100.0 or self.turn > self.max_turns:
            self.game_over = True
            if self.yield_rate >= 90.0:
                grade = "🏆 [S등급] 수석 화학공정 엔지니어"
                msg = f"축하합니다! 폭발 없이 최종 수율 {self.yield_rate:.1f}%를 달성했습니다!\n최적의 온도 제어와 반응 속도 밸런스를 입증했습니다."
            elif self.yield_rate >= 70.0:
                grade = "🥈 [A등급] 일반 엔지니어"
                msg = f"안전하게 운전을 마쳤으나, 최종 수율이 {self.yield_rate:.1f}%로 목표치(90%)에 약간 미달했습니다."
            else:
                grade = "🥉 [C등급] 개선 권고"
                msg = f"최종 수율이 {self.yield_rate:.1f}%에 머물렀습니다. 냉각 조절을 재검토하세요."

            messagebox.showinfo(grade, msg)
            self.prompt_restart()

    def prompt_restart(self):
        if messagebox.askyesno("다시 도전", "반응기 공정을 처음부터 다시 시작하시겠습니까?"):
            self.reset_game_state()
            self.log_text.config(state="normal")
            self.log_text.delete("1.0", "end")
            self.log_text.config(state="disabled")
            for msg in self.log_messages:
                self.log(msg)
            self.update_ui()
        else:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ReactorGame(root)
    root.mainloop()

