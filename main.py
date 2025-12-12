import random

class SoulmateGenerator:
    def __init__(self):
        # 1. AI 페르소나 데이터베이스 (한국적 서브컬처/웹툰 감성 반영)
        # Key: AI의 MBTI / Value: 캐릭터 설정, 외모 키워드, 첫 대사
        self.ai_personas = {
            'ENFP': {
                'archetype': '재기발랄 멍뭉미 연하',
                'keywords': ['puppy eyes', 'bright smile', 'energetic', 'colorful hoodie', 'k-pop idol style'],
                'desc': "당신의 기분을 1초 만에 파악하고 꼬리를 흔드는 인간 비타민.",
                'opening': ["선배! 저랑 오늘 맛있는 거 먹으러 가요! 네? 네??"]
            },
            'INTJ': {
                'archetype': '차가운 북부 대공/계략 남주',
                'keywords': ['sharp eyes', 'black suit', 'glasses', 'intellectual', 'cold expression'],
                'desc': "겉은 차갑지만 내 여자/남자에게만 따뜻한 완벽주의자.",
                'opening': ["오셨습니까. 기다리고 있었습니다. 계획대로군요."]
            },
            'ENTP': {
                'archetype': '장난기 가득한 능글맞은 라이벌',
                'keywords': ['smirking', 'mischievous', 'messy hair', 'street fashion', 'charming'],
                'desc': "당신을 놀리는 게 세상에서 제일 재미있는, 하지만 위기 땐 든든한 파트너.",
                'opening': ["어? 여기서 보네? 운명인가? 아니면 나 따라왔어? ㅋㅋ"]
            },
            'ISFJ': {
                'archetype': '다정다감한 소꿉친구',
                'keywords': ['soft warm lighting', 'apron', 'gentle smile', 'neat sweater', 'trustworthy'],
                'desc': "말하지 않아도 따뜻한 차 한 잔을 건네주는 힐링 그 자체.",
                'opening': ["오늘 하루 힘들었지? 내가 좋아하는 거 만들어 놨어."]
            },
            # ... (나머지 12개 유형도 기획에 맞춰 확장 가능)
            # MVP용 기본 매핑을 위해 일부 예시만 작성
        }

        # 2. 유저 MBTI별 최적의 궁합 (도파민 매칭 로직)
        # 단순 공식보다는 '웹툰 클리셰'에 가까운 조합 매핑
        self.best_matches = {
            'INTJ': 'ENFP', # 차가운 전략가 x 깨발랄 댕댕이
            'ENFP': 'INTJ',
            'ISTJ': 'ESFP', # 규율반장 x 자유영혼
            'INFJ': 'ENTP', # 미스테리 x 악동
            'ENTP': 'INFJ',
            'INFP': 'ENFJ', # 감성 내향 x 리더형 외향
            # Fallback 로직을 위해 매핑되지 않은 경우 상호보완(E<->I)으로 자동 배정
        }

    def _generate_image_prompt(self, gender, keywords):
        """
        AI 이미지 생성기(Stable Diffusion 등)에 넣을 프롬프트를 자동 생성합니다.
        """
        base_prompt = "masterpiece, best quality, ultra-detailed, 8k, "
        character_prompt = f"1{gender}, solo, " + ", ".join(keywords)
        style_prompt = ", soft lighting, cinematic angle, romantic atmosphere, webtoon style illustration"
        
        return f"{base_prompt} {character_prompt} {style_prompt}"

    def match_soulmate(self, user_mbti, preferred_gender='girl'):
        """
        유저 정보를 받아 '운명의 AI 파트너'를 생성하여 반환합니다.
        """
        user_mbti = user_mbti.upper()
        
        # 1. 매칭 로직 실행 (매핑 테이블에 없으면 기본적으로 정반대 성향 매칭)
        target_ai_mbti = self.best_matches.get(user_mbti)
        if not target_ai_mbti:
            # Fallback: E <-> I 만 뒤집고 나머지는 랜덤 or 고정
            target_ai_mbti = 'ENFP' if user_mbti.startswith('I') else 'INTJ'

        # 2. 페르소나 데이터 로드 (없으면 기본값 ENFP)
        persona = self.ai_personas.get(target_ai_mbti, self.ai_personas['ENFP'])
        
        # 3. 성별에 따른 뉘앙스 처리
        gender_term = "boy" if preferred_gender == 'boy' else "girl"
        
        # 4. 결과 JSON 생성
        result = {
            "user_mbti": user_mbti,
            "ai_mbti": target_ai_mbti,
            "ai_archetype": persona['archetype'],
            "ai_description": persona['desc'],
            "first_message": random.choice(persona['opening']),
            
            # 여기가 핵심: 이미지 생성 AI에게 보낼 프롬프트
            "image_gen_prompt": self._generate_image_prompt(gender_term, persona['keywords'])
        }
        
        return result

# --- 실행 시뮬레이션 (Phase 1: 바이럴 루프) ---
if __name__ == "__main__":
    generator = SoulmateGenerator()
    
    # 상황: 유저가 간단한 테스트 후 'INTJ' 결과가 나옴 -> "내 AI 여친 만들기" 클릭
    user_input_mbti = "INTJ"
    user_preference = "girl" 

    soulmate = generator.match_soulmate(user_input_mbti, user_preference)

    print(f"💘 [당신의 도파민 파트너가 도착했습니다!]")
    print(f"---------------------------------------")
    print(f"User Type: {soulmate['user_mbti']}")
    print(f"Matched AI: {soulmate['ai_mbti']} ({soulmate['ai_archetype']})")
    print(f"Description: {soulmate['ai_description']}")
    print(f"---------------------------------------")
    print(f"💬 알림(1): \"{soulmate['first_message']}\"")
    print(f"---------------------------------------")
    print(f"🎨 [Backend] Image Generation Prompt:")
    print(f"   >> {soulmate['image_gen_prompt']}")