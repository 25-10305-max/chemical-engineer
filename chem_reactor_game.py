"""
[화학공학 미니게임] '스마트 반응기 폭발 방지 및 최고 수율 달성 게임'
- 목표: 발열 반응을 진행하는 화학 반응기의 냉각수/교반 속도를 조절하여
        '열폭주(폭발)'를 막고 목표 수율(90% 이상)을 달성하기!
"""

import time
import os

def clear_screen():
    # 윈도우/리눅스 화면 정리
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("=" * 60)
    print(" 🎮  [화학공학 게임] 스마트 CSTR 반응기 엔지니어 챌린지! ")
    print("=" * 60)
    print(" 당신은 신입 화학공정 엔지니어입니다!")
    print(" 발열 반응(Exothermic Reaction)이 일어나는 반응기를 제어하여")
    print(" 폭발(100℃ 초과)을 막고, 반응 수율 90% 이상을 달성하세요!\n")
    print(" ⚠️ 주의:")
    print("  - 온도가 100℃를 넘으면 '열폭주(Thermal Runaway)'로 폭발합니다! 💥")
    print("  - 온도가 30℃ 이하로 떨어지면 반응이 멈춰 얼어붙습니다! ❄️")
    print("  - 온도가 높을수록 반응 속도가 빨라져 수율이 빠르게 오릅니다. 🔥")
    print("=" * 60)
    input("\n[Enter] 키를 누르면 공정이 시작됩니다...")

    temp = 45.0         # 현재 반응기 온도 (℃)
    yield_rate = 0.0    # 반응 수율 (%)
    turn = 1
    max_turns = 10      # 총 10턴

    while turn <= max_turns:
        clear_screen()
        # 온도 상태 게이지 바 제작
        gauge_len = int(temp / 5)
        gauge = "█" * gauge_len + "░" * (20 - gauge_len)

        print(f"\n⏱️  [턴 {turn}/{max_turns}] 반응기 운전 현황")
        print("-" * 50)
        print(f" 🌡️ 반응기 내부 온도 : {temp:.1f} ℃  [{gauge}]")
        print(f" ⚗️ 생성물 반응 수율 : {yield_rate:.1f} %")
        print("-" * 50)

        # 위험 경고
        if temp >= 80:
            print(" 🚨 [위험 경고] 온도가 너무 높습니다! 폭발 위험! 냉각이 시급합니다!")
        elif temp <= 40:
            print(" ⚠️ [경고] 반응 속도가 너무 느립니다! 온도를 올려야 합니다.")
        else:
            print(" ✅ [안정] 적정 온도 구간에서 최적의 반응이 진행 중입니다.")

        print("\n⚙️ 이번 턴의 운전 조작을 선택하세요:")
        print(" 1) [강력 냉각] 냉각수 밸브 최대로 열기 (온도 급감, 수율 미미)")
        print(" 2) [정상 냉각] 냉각수 밸브 유지 (온도 유지/소폭 하락, 수율 안정적)")
        print(" 3) [교반 가속] 교반기 모터 속도 증가 (반응 활성화, 온도 소폭 상승, 수율 보통)")
        print(" 4) [촉매 추가] 반응 촉매 투입! (온도 급상승! 수율 대폭 증가!)")

        choice = input("\n👉 선택 (1~4번 입력): ").strip()

        # 반응 메커니즘 (발열 반응 모델링)
        # 기본적으로 매 턴 발열로 온도가 +8℃ 상승하려는 경향이 있음
        exotherm = 8.0 

        if choice == "1":
            print("\n>> ❄️ 냉각수를 대량 공급합니다! (-18℃)")
            temp += exotherm - 18.0
            yield_rate += max(1.0, (temp / 25.0) * 3)
        elif choice == "2":
            print("\n>> 💧 냉각수를 적정량 공급합니다. (-9℃)")
            temp += exotherm - 9.0
            yield_rate += max(2.0, (temp / 20.0) * 5)
        elif choice == "3":
            print("\n>> 🌪️ 교반기를 빠르게 회전시켜 반응을 촉진합니다! (+5℃)")
            temp += exotherm + 5.0
            yield_rate += max(3.0, (temp / 18.0) * 7)
        elif choice == "4":
            print("\n>> 🧪 반응 촉매를 대량 투입했습니다!! (+18℃, 수율 대폭 상승)")
            temp += exotherm + 18.0
            yield_rate += max(5.0, (temp / 15.0) * 11)
        else:
            print("\n>> ⚠️ 조작 실수! 반응기를 방치했습니다. (온도 상승)")
            temp += exotherm
            yield_rate += 2.0

        # 온도 및 반응 한계값 보정
        if yield_rate > 100.0:
            yield_rate = 100.0

        time.sleep(1.2)

        # 게임 오버 조건 체크
        if temp > 100.0:
            clear_screen()
            print("💥" * 25)
            print(" 💥💥💥 [비상 사태] 열폭주(Thermal Runaway) 발생! 💥💥💥")
            print(" 반응기 내부 온도가 100℃를 초과하여 압력을 이기지 못하고 폭발했습니다!")
            print(f" 최종 기록: 턴 {turn}에서 중단 / 도달 수율: {yield_rate:.1f}%")
            print("💥" * 25)
            return

        if temp < 30.0:
            clear_screen()
            print("❄️" * 25)
            print(" ❄️❄️❄️ [공정 중단] 반응기 동결! ❄️❄️❄️")
            print(" 온도가 30℃ 밑으로 떨어져 활성화 에너지를 넘지 못하고 반응이 정지했습니다.")
            print(f" 최종 기록: 턴 {turn}에서 중단 / 도달 수율: {yield_rate:.1f}%")
            print("❄️" * 25)
            return

        # 조기 수율 100% 달성 성공
        if yield_rate >= 100.0:
            break

        turn += 1

    # 최종 결과 화면
    clear_screen()
    print("=" * 60)
    print(" 🎉  공정 운전 종료 - 엔지니어 성적표 ")
    print("=" * 60)
    print(f" - 최종 반응기 온도 : {temp:.1f} ℃")
    print(f" - 최종 생성물 수율 : {yield_rate:.1f} %")
    print("-" * 60)

    if yield_rate >= 90.0:
        print(" 🏆 [SUCCESS] 특급 화학공정 엔지니어!")
        print(" 폭발 없이 안전하게 목표 수율(90% 이상)을 초과 달성했습니다!")
    elif yield_rate >= 70.0:
        print(" 🥈 [PASS] 보통 엔지니어")
        print(" 폭발은 막았으나, 온도 제어가 보수적이어서 목표 수율에 살짝 못 미쳤습니다.")
    else:
        print(" 🥉 [FAIL] 공정 개선 필요")
        print(" 냉각을 너무 많이 하여 반응이 충분히 일어나지 못했습니다.")
    print("=" * 60)


if __name__ == "__main__":
    main()

