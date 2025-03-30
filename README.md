# SinogramReconstruction

이 프로젝트는 제조업 결함 탐지를 위한 시노그램(Sinogram)에서 이미지를 재구성하는 코드입니다. 필터링된 역투영(Filtered Back-Projection) 방법을 사용하여 시노그램을 원래 이미지로 복원합니다.

## 개요

이 코드는 다음과 같은 주요 기능을 제공합니다:

1. 시노그램 이미지로부터 원본 이미지 복원
2. 라돈 변환(Radon Transform)을 사용한 시노그램 생성
3. 필터링된 역투영(Filtered Back-Projection) 알고리즘 구현
4. 해밍 윈도우(Hamming Window)를 적용한 이미지 개선

## 주요 함수

- `radon(image, steps)`: 이미지를 시노그램으로 변환
- `fft_translate(projs)`: 시노그램을 주파수 도메인으로 변환
- `ramp_filter(ffts)`: 1차원 FFT에 램프 필터 적용
- `inverse_fft_translate(operator)`: 1차원 역 FFT 적용
- `back_project(operator)`: 역투영을 통한 이미지 재구성

## 이미지 재구성 과정

1. 시노그램 로딩
2. 필터링 없는 백프로젝션 복원 (비교용)
3. 시노그램의 1차원 진폭 스펙트럼 계산
4. 램프 필터링된 1차원 진폭 스펙트럼 계산
5. 1차원 역푸리에변환 수행
6. 백프로젝션 복원 수행
7. 해밍윈도우 적용한 개선된 복원 이미지 생성

## 필요한 라이브러리

- NumPy
- imutils
- scikit-image
- SciPy
- matplotlib
- imageio

## 사용 방법

1. 필요한 라이브러리 설치:
```bash
pip install numpy imutils scikit-image scipy matplotlib imageio
```

2. 시노그램 이미지 준비 (예: 'sinog.png')

3. 코드 실행:
```bash
python sinogram_reconstruction.py
```

## 결과

코드 실행 시 다음과 같은 이미지들이 순차적으로 표시됩니다:
- 원본 시노그램
- 필터링 없는 백프로젝션 복원 이미지
- 시노그램의 주파수 도메인 표현
- 램프 필터링된 주파수 도메인
- 램프 필터링된 시노그램의 공간 도메인 표현
- 최종 복원된 이미지
- 해밍윈도우 적용 복원 이미지

## 참고 자료

이 코드는 다음 저장소를 참고하였습니다:
- [Sinogram-to-Image](https://github.com/IanB14/Sinogram-to-Image)

## 용도

이 코드는 다음과 같은 분야에 활용될 수 있습니다:
- 산업용 CT 스캔에서 결함 탐지
- 비파괴 검사(NDT) 시스템
- 의료 이미지 처리
- 제조업 품질 관리

## 라이센스

MIT 라이센스