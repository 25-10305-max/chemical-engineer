"""
[화학공학 & 화학II 물질과 에너지 미니게임]
타이틀: 그린 화학공장: 물질수지 & 에너지수지 최적화 챌린지 (Green Eco-Plant)
- 고2 화학II '물질과 에너지(반응엔탈피, 헤스의 법칙, 열역학, 열교환기)' 핵심 개념 연계
- GUI 기반 (Tkinter, 추가 설치 불필요)
"""

import tkinter as tk
from tkinter import ttk, messagebox

class ChemicalBalanceGame:
    def __init__(self, root):
        self.root = root
        self.root.title("화학공학 탐구: 물질수지와 에너지수지 최적화 공정 시뮬레이터")
        self.root.geometry("680x760")
        self.root.resizable(False, False)
        self.root.configure(bg="#f1f4f8")

        self.reset_game_state()
        self.create_widgets()
        self.update_ui()

    def reset_game_state(self):
        # [물질 수지]
        self.feed_A = 100.0        # 주원료 A 잔여량 (kmol)
        self.product = 0.0         # 생성물 순수 생산량 (kmol) - 목표: 80 kmol
        self.byproduct = 0.0       # 폐기물/부반응 부산물 (kmol) - 최소화 목표

        # [에너지 수지]
        # 반응엔탈피(ΔH): -150 kJ/mol (강한 발열 반응)
        self.reactor_heat = 50.0   # 반응기 내부 잉여 열에너지 (MJ, 적정 40~70)
        self.electric_cost = 0.0   # 공정 전력 소비 비용 (kWh 누적)
        self.heat_recovery = 0.0   # 열교환기 폐열 회수량 (MJ)

        self.day = 1               # 운전 일차 (총 10일)
        self.max_days = 10
        self.game_over = False

    def create_widgets(self):
        # 헤더
        header = tk.Frame(self.root, bg="#1a365d", pady=14)
        header.pack(fill="x")

        tk.Label(
            header, 
            text="🌿 그린 화학공장: 물질수지 & 에너지수지 챌린지", 
            font=("맑은 고딕", 15, "bold"), fg="#ffffff", bg="#1a365d"
        ).pack()

        tk.Label(
            header, 
            text="화학II [물질과 에너지: 반응 엔탈피(ΔH), 폐열 회수(열교환기), 질량보존의 법칙]", 
            font=("맑은 고딕", 9), fg="#cbd5e0", bg="#1a365d"
        ).pack(pady=2)

        # 1. 물질 수지(Mass Balance) 카드
        mass_frame = tk.LabelFrame(
            self.root, 
            text=" ⚖️ [물질 수지 (Mass Balance)] 반응물 투입 vs 생성물 생산 ", 
            font=("맑은 고딕", 10, "bold"), bg="white", padx=15, pady=8
        )
        mass_frame.pack(fill="x", padx=16, pady=6)

        m_grid = tk.Frame(mass_frame, bg="white")
        m_grid.pack(fill="x")

        tk.Label(m_grid, text="남은 원료 A:", font=("맑은 고딕", 9), bg="white").grid(row=0, column=0, sticky="w")
        self.lbl_feed = tk.Label(m_grid, text="100.0 kmol", font=("맑은 고딕", 9, "bold"), fg="#2b6cb0", bg="white")
        self.lbl_feed.grid(row=0, column=1, sticky="w", padx=10)

        tk.Label(m_grid, text="생성물 B (목표 80 kmol):", font=("맑은 고딕", 9), bg="white").grid(row=0, column=2, sticky="w")
        self.lbl_product = tk.Label(m_grid, text="0.0 kmol", font=("맑은 고딕", 9, "bold"), fg="#2f855a", bg="white")
        self.lbl_product.grid(row=0, column=3, sticky="w", padx=10)

        tk.Label(m_grid, text="부반응 폐기물 C:", font=("맑은 고딕", 9), bg="white").grid(row=1, column=0, sticky="w", pady=4)
        self.lbl_byproduct = tk.Label(m_grid, text="0.0 kmol", font=("맑은 고딕", 9, "bold"), fg="#c53030", bg="white")
        self.lbl_byproduct.grid(row=1, column=1, sticky="w", padx=10, pady=4)

        # 생성물 달성도 프로그레스바
        self.prod_bar = ttk.Progressbar(mass_frame, maximum=80, length=600)
        self.prod_bar.pack(fill="x", pady=4)

        # 2. 에너지 수지(Energy Balance) 카드
        energy_frame = tk.LabelFrame(
            self.root, 
            text=" 🔥 [에너지 수지 (Energy Balance)] 반응열(ΔH) 관리 & 폐열 재활용 ", 
            font=("맑은 고딕", 10, "bold"), bg="white", padx=15, pady=8
        )
        energy_frame.pack(fill="x", padx=16, pady=6)

        e_grid = tk.Frame(energy_frame, bg="white")
        e_grid.pack(fill="x")

        tk.Label(e_grid, text="반응기 축적 열에너지:", font=("맑은 고딕", 9), bg="white").grid(row=0, column=0, sticky="w")
        self.lbl_heat = tk.Label(e_grid, text="50.0 MJ (적정 40~70)", font=("맑은 고딕", 9, "bold"), fg="#dd6b20", bg="white")
        self.lbl_heat.grid(row=0, column=1, sticky="w", padx=10)

        tk.Label(e_grid, text="폐열 회수량 (친환경):", font=("맑은 고딕", 9), bg="white").grid(row=0, column=2, sticky="w")
        self.lbl_recovery = tk.Label(e_grid, text="0.0 MJ", font=("맑은 고딕", 9, "bold"), fg="#319795", bg="white")
        self.lbl_recovery.grid(row=0, column=3, sticky="w", padx=10)

        tk.Label(e_grid, text="냉각 펌프 소비전력:", font=("맑은 고딕", 9), bg="white").grid(row=1, column=0, sticky="w", pady=4)
        self.lbl_cost = tk.Label(e_grid, text="0.0 kWh", font=("맑은 고딕", 9, "bold"), fg="#718096", bg="white")
        self.lbl_cost.grid(row=1, column=1, sticky="w", padx=10, pady=4)

        self.heat_bar = ttk.Progressbar(energy_frame, maximum=100, length=600)
        self.heat_bar.pack(fill="x", pady=4)

        # 상태 메시지
        self.status_banner = tk.Label(
            self.root, 
            text="운전 1일차: 공정 엔지니어의 첫 번째 수지(Balance) 결정을 내려주세요.", 
            font=("맑은 고딕", 10, "bold"), bg="#ebf8ff", fg="#2b6cb0", pady=6
        )
        self.status_banner.pack(fill="x", padx=16, pady=4)

        # 3. 공정 제어 선택 버튼들 (화학공학 물질-에너지 균형 의사결정)
        action_frame = tk.LabelFrame(
            self.root, 
            text=" ⚙️ 공정 제어 및 물질/에너지 조작 선택 ", 
            font=("맑은 고딕", 10, "bold"), bg="white", padx=15, pady=8
        )
        action_frame.pack(fill="x", padx=16, pady=6)

        btn_box = tk.Frame(action_frame, bg="white")
        btn_box.pack(fill="x")

        # 버튼 1: 표준 반응 운전
        b1 = tk.Button(
            btn_box, 
            text="1️⃣ [표준 수지 반응]\n원료 투입 10 kmol (정량적 반응, 발열 +15 MJ)", 
            font=("맑은 고딕", 9), bg="#e2e8f0", relief="groove", height=2,
            command=lambda: self.run_turn(1)
        )
        b1.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")

        # 버튼 2: 열교환기 연계 운전 (에너지 재활용)
        b2 = tk.Button(
            btn_box, 
            text="2️⃣ [열교환기 폐열 회수 운전]\n반응열 -20 MJ 회수 및 예열 활용 (친환경 에너지 절감)", 
            font=("맑은 고딕", 9), bg="#feebc8", relief="groove", height=2,
            command=lambda: self.run_turn(2)
        )
        b2.grid(row=0, column=1, padx=4, pady=4, sticky="nsew")

        # 버튼 3: 흡열성 불순물 정제 및 고효율 촉매
        b3 = tk.Button(
            btn_box, 
            text="3️⃣ [고효율 촉매 + 물질 정제]\n선택도 증가(부산물 최소화), 흡열 공정 연계 (-15 MJ)", 
            font=("맑은 고딕", 9), bg="#c6f6d5", relief="groove", height=2,
            command=lambda: self.run_turn(3)
        )
        b3.grid(row=1, column=0, padx=4, pady=4, sticky="nsew")

        # 버튼 4: 급속 비상 냉각수 투입
        b4 = tk.Button(
            btn_box, 
            text="4️⃣ [비상 칠러 냉각수 가동]\n열에너지 급랭 (-35 MJ), 전력 소비 증가 (50 kWh)", 
            font=("맑은 고딕", 9), bg="#bee3f8", relief="groove", height=2,
            command=lambda: self.run_turn(4)
        )
        b4.grid(row=1, column=1, padx=4, pady=4, sticky="nsew")

        btn_box.columnconfigure(0, weight=1)
        btn_box.columnconfigure(1, weight=1)

        # 로그창
        log_frame = tk.LabelFrame(self.root, text=" 📜 공정 물질·에너지 물질수지표 일지 ", font=("맑은 고딕", 9), bg="white", padx=8, pady=4)
        log_frame.pack(fill="both", expand=True, padx=16, pady=(4, 12))

        self.log_txt = tk.Text(log_frame, height=5, font=("Consolas", 8), state="disabled", bg="#fafafa", relief="flat")
        self.log_txt.pack(fill="both", expand=True)

    def write_log(self, text):
        self.log_txt.config(state="normal")
        self.log_txt.insert("end", f"> {text}\n")
        self.log_txt.see("end")
        self.log_txt.config(state="disabled")

    def run_turn(self, choice):
        if self.game_over:
            return

        if self.feed_A <= 0:
            self.write_log("원료 A가 모두 소진되었습니다.")
            self.finish_game()
            return

        # [물질과 에너지 메커니즘]
        # A(원료) -> B(주생성물) + C(부산물) : ΔH < 0 (발열)
        if choice == 1:
            # 표준 반응
            feed_used = min(12.0, self.feed_A)
            self.feed_A -= feed_used
            b_made = feed_used * 0.82   # 선택도 82%
            c_made = feed_used * 0.18   # 부산물 18%
            self.product += b_made
            self.byproduct += c_made
            self.reactor_heat += 16.0   # 발열
            self.electric_cost += 10.0
            self.write_log(f"[{self.day}일차 표준운전] 원료 {feed_used:.1f}kmol 투입 -> 생성물 +{b_made:.1f}kmol, 발열 +16MJ")

        elif choice == 2:
            # 열교환기 폐열 회수
            feed_used = min(10.0, self.feed_A)
            self.feed_A -= feed_used
            b_made = feed_used * 0.85
            c_made = feed_used * 0.15
            self.product += b_made
            self.byproduct += c_made
            recovered = 20.0
            self.heat_recovery += recovered
            self.reactor_heat += (14.0 - recovered) # 발열 14MJ 중 20MJ 회수하여 냉각 효과
            self.electric_cost += 12.0
            self.write_log(f"[{self.day}일차 열교환기 운전] 폐열 {recovered}MJ 회수 성공! 공정 예열로 재활용됨")

        elif choice == 3:
            # 고효율 촉매 (선택도 극대화, 물질수지 최적화)
            feed_used = min(11.0, self.feed_A)
            self.feed_A -= feed_used
            b_made = feed_used * 0.94   # 선택도 94%!
            c_made = feed_used * 0.06
            self.product += b_made
            self.byproduct += c_made
            self.reactor_heat -= 12.0   # 흡열 공정 연계로 열 감쇠
            self.electric_cost += 20.0
            self.write_log(f"[{self.day}일차 촉매정제] 수율 94% 달성 (+{b_made:.1f}kmol), 부산물 억제, 반응기 열 -12MJ")

        elif choice == 4:
            # 비상 칠러
            self.reactor_heat -= 35.0
            self.electric_cost += 55.0
            self.write_log(f"[{self.day}일차 냉각수 급랭] 전력 55kWh 소비, 반응열 급랭 -35MJ")

        # 하루 경과
        self.day += 1
        self.update_ui()
        self.check_limits()

    def update_ui(self):
        self.lbl_feed.config(text=f"{self.feed_A:.1f} kmol")
        self.lbl_product.config(text=f"{self.product:.1f} kmol")
        self.lbl_byproduct.config(text=f"{self.byproduct:.1f} kmol")
        self.prod_bar['value'] = min(self.product, 80)

        self.lbl_heat.config(text=f"{self.reactor_heat:.1f} MJ")
        self.lbl_recovery.config(text=f"{self.heat_recovery:.1f} MJ")
        self.lbl_cost.config(text=f"{self.electric_cost:.1f} kWh")
        self.heat_bar['value'] = min(max(self.reactor_heat, 0), 100)

        # 위험 배너 경고
        if self.reactor_heat >= 80:
            self.status_banner.config(
                text=f"🚨 [열에너지 과열 경고] 반응기 잉여열({self.reactor_heat:.1f}MJ) 위험! 열교환기 또는 냉각이 필수!",
                bg="#fed7d7", fg="#c53030"
            )
        elif self.reactor_heat <= 30:
            self.status_banner.config(
                text=f"❄️ [에너지 부족 경고] 열량이 너무 낮아 반응 속도가 급감하고 응고될 수 있습니다.",
                bg="#e2e8f0", fg="#4a5568"
            )
        else:
            self.status_banner.config(
                text=f"운전 {min(self.day, self.max_days)}일차: 최적 물질-에너지 균형(40~70 MJ) 구간 운전 중.",
                bg="#ebf8ff", fg="#2b6cb0"
            )

    def check_limits(self):
        # 에너지 수지 실패 (100 MJ 초과 폭발)
        if self.reactor_heat > 100.0:
            self.game_over = True
            messagebox.showerror(
                "💥 에너지 수지 불균형 폭발!",
                f"반응열(ΔH)의 방출 속도가 제거 속도를 압도하여 열폭주가 발생했습니다!\n"
                f"최종 생성물: {self.product:.1f} kmol\n"
                f"화학II 연계: '반응 엔탈피와 열역학 제1법칙(에너지 보존 법칙)'에 의해\n"
                f"발열량만큼 계의 에너지를 외부로 전달하지 못하면 폭발합니다."
            )
            self.prompt_restart()
            return

        # 반응 정지 (20 MJ 이하)
        if self.reactor_heat < 20.0:
            self.game_over = True
            messagebox.showwarning(
                "❄️ 에너지 부족으로 반응 정지",
                f"반응기 열에너지가 부족하여 활성화 에너지를 극복하지 못했습니다.\n"
                f"최종 생성물: {self.product:.1f} kmol"
            )
            self.prompt_restart()
            return

        # 10일 종료 또는 목표 80 kmol 조기 달성
        if self.day > self.max_days or self.product >= 80.0:
            self.finish_game()

    def finish_game(self):
        self.game_over = True
        # 친환경 & 경제성 종합 점수 산출
        # 점수 = (생성물 * 1.5) + (폐열회수 * 1.2) - (부산물 * 2.0) - (전력소비 * 0.5)
        score = (self.product * 1.5) + (self.heat_recovery * 1.2) - (self.byproduct * 2.0) - (self.electric_cost * 0.3)
        
        grade = "🏆 [S등급] 스마트 그린 화공 엔지니어" if score >= 100 else ("🥈 [A등급] 우수 엔지니어" if score >= 70 else "🥉 [B등급] 보통 운전원")

        msg = (
            f"=== 10일간의 물질·에너지 공정 운전 성적표 ===\n\n"
            f"1. 물질 수지 성과:\n"
            f" - 순수 생성물(B) 생산량: {self.product:.1f} / 80.0 kmol\n"
            f" - 부반응 폐기물(C) 배출: {self.byproduct:.1f} kmol (적을수록 좋음)\n\n"
            f"2. 에너지 수지 성과:\n"
            f" - 폐열 회수량(친환경 에너지): {self.heat_recovery:.1f} MJ\n"
            f" - 누적 전력 소모: {self.electric_cost:.1f} kWh\n\n"
            f"종합 환경·경제성 점수: {score:.1f}점\n"
            f"결과: {grade}"
        )
        messagebox.showinfo("공정 운전 완료", msg)
        self.prompt_restart()

    def prompt_restart(self):
        if messagebox.askyesno("재도전", "공정을 초기화하고 다시 시작하시겠습니까?"):
            self.reset_game_state()
            self.log_txt.config(state="normal")
            self.log_txt.delete("1.0", "end")
            self.log_txt.config(state="disabled")
            self.update_ui()
        else:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChemicalBalanceGame(root)
    root.mainloop()

