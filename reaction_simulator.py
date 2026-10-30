"""
반응공학 시뮬레이터: 반응 속도론(반응 차수) 및 아레니우스 식을 이용한 농도 변화 시뮬레이션
화학공학 / 화학II 연계 탐구 활동용 프로그램
"""

import math
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Windows 기본 맑은 고딕)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


def calculate_rate_constant(A, Ea, T):
    """
    아레니우스 방정식 (Arrhenius Equation): k = A * exp(-Ea / (R * T))
    A: 잦음률 (Frequency factor)
    Ea: 활성화 에너지 (J/mol)
    T: 절대온도 (K)
    R: 기체상수 (8.314 J/(mol*K))
    """
    R = 8.314
    return A * math.exp(-Ea / (R * T))


def simulate_reaction(order, k, C0, total_time, dt=0.1):
    """
    오일러 방법(Euler's Method)을 이용한 미분방정식 수치해석:
    - 0차 반응: -d[A]/dt = k
    - 1차 반응: -d[A]/dt = k * [A]
    - 2차 반응: -d[A]/dt = k * [A]^2
    """
    times = [0.0]
    concentrations = [C0]
    
    current_time = 0.0
    current_C = C0
    
    while current_time < total_time:
        if order == 0:
            rate = k
        elif order == 1:
            rate = k * current_C
        elif order == 2:
            rate = k * (current_C ** 2)
        else:
            raise ValueError("지원하지 않는 반응 차수입니다.")
        
        # dC/dt = -rate => C_next = C - rate * dt
        next_C = current_C - rate * dt
        if next_C < 0:
            next_C = 0.0
            
        current_time += dt
        current_C = next_C
        
        times.append(current_time)
        concentrations.append(current_C)
        
        if current_C <= 0:
            break
            
    return times, concentrations


def main():
    print("=" * 65)
    print("  [화학공학 탐구] 반응 속도론 및 아레니우스 식 기반 반응기 시뮬레이터")
    print("=" * 65)
    print("고등학교 화학II의 '반응 속도'와 '화학공학의 회분식 반응기(Batch Reactor)'를 모델링합니다.\n")

    # 기본 파라미터 안내 및 입력
    print("[1] 기본 물성치 설정")
    A = 1.0e7           # 잦음률 (1/s 가정)
    Ea = 50000.0        # 활성화 에너지: 50 kJ/mol = 50,000 J/mol
    print(f" - 활성화 에너지(Ea): {Ea / 1000} kJ/mol")
    print(f" - 잦음률(A): {A:.1e}")
    
    try:
        order = int(input("\n반응 차수를 입력하세요 (0, 1, 2 중 선택, 기본값 1): ") or "1")
        C0 = float(input("초기 반응물 농도 [A]0 (mol/L, 기본값 1.0): ") or "1.0")
        total_time = float(input("총 반응 진행 시간 (초, 기본값 60): ") or "60")
    except ValueError:
        print("잘못된 입력입니다. 기본값으로 실행합니다.")
        order, C0, total_time = 1, 1.0, 60.0

    # 3가지 온도 조건에서 반응 비교 (예: 25℃, 45℃, 65℃)
    temperatures_celsius = [25, 45, 65]
    
    plt.figure(figsize=(10, 6))
    
    print("\n[2] 시뮬레이션 계산 결과")
    print("-" * 65)
    for T_c in temperatures_celsius:
        T_k = T_c + 273.15
        k = calculate_rate_constant(A, Ea, T_k)
        t_data, c_data = simulate_reaction(order, k, C0, total_time, dt=0.05)
        
        # 최종 농도 및 전환율 계산
        conversion = ((C0 - c_data[-1]) / C0) * 100
        print(f"온도: {T_c:2d}℃ ({T_k:.2f}K) | 반응속도상수(k): {k:.4e} | 최종 전화율: {conversion:.2f}%")
        
        plt.plot(t_data, c_data, label=f'{T_c}℃ (k = {k:.2e})', linewidth=2)
        
    print("-" * 65)
    
    # 그래프 시각화 스타일링
    plt.title(f'{order}차 반응에서의 온도별 반응물 농도 변화 ([A]₀ = {C0} M)', fontsize=14, pad=15)
    plt.xlabel('시간 (초, s)', fontsize=12)
    plt.ylabel('반응물 농도 [A] (mol/L)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=11)
    
    output_filename = "reaction_simulation.png"
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"\n[3] 결과 그래프가 '{output_filename}' 파일로 저장되었습니다.")
    
    # 윈도우 환경에서 그래프 창 띄우기
    plt.show()


if __name__ == "__main__":
    main()

