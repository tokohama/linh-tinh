import streamlit as str

# 1. Kh?i t?o co s? d? li?u món an m?u kèm hình ?nh minh h?a công khai
MEALS_DB = [
    {
        "name": "?c gà áp ch?o & Bông c?i xanh",
        "calories": 350, "protein": 40, "carbs": 15, "fat": 5, "sodium": 120, "purine": "Th?p", "gi": "Th?p",
        "image": "https://unsplash.com",
        "tags": ["Gi?m cân", "Tang co"]
    },
    {
        "name": "Salad cá h?i bo",
        "calories": 450, "protein": 30, "carbs": 10, "fat": 25, "sodium": 200, "purine": "V?a", "gi": "Th?p",
        "image": "https://unsplash.com",
        "tags": ["Gi?m cân", "S?c kh?e tim m?ch"]
    },
    {
        "name": "Cháo y?n m?ch chu?i và h?t chia",
        "calories": 300, "protein": 10, "carbs": 55, "fat": 6, "sodium": 10, "purine": "Th?p", "gi": "V?a",
        "image": "https://unsplash.com",
        "tags": ["Gi?m cân"]
    },
    {
        "name": "Th?t bò bit t?t & Khoai tây nghi?n",
        "calories": 650, "protein": 45, "carbs": 40, "fat": 30, "sodium": 450, "purine": "Cao", "gi": "Cao",
        "tags": ["Tang co", "Tang cân"]
    }
]

# Giao di?n Mini App
str.set_page_config(page_title="Fitness & Nutrition Mini App", page_icon="??", layout="wide")
str.title("?? Mini App Theo Dõi Luy?n T?p & Dinh Du?ng Cá Nhân Hóa")

# Chia c?t b? c?c: Trái (Nh?p li?u) - Ph?i (K?t qu? & G?i ý)
col1, col2 = str.columns([1, 2])

with col1:
    str.header("?? Thông tin ngu?i dùng")
    gender = str.radio("Gi?i tính", ["Nam", "N?"])
    age = str.number_input("Tu?i", min_value=1, max_value=100, value=25)
    weight = str.number_input("Cân n?ng (kg)", min_value=30.0, max_value=200.0, value=60.0)
    height = str.number_input("Chi?u cao (cm)", min_value=100.0, max_value=250.0, value=165.0)
    
    activity = str.selectbox("T?n su?t v?n d?ng", [
        "Ít v?n d?ng (Van phòng)",
        "V?n d?ng nh? (1-3 ngày/tu?n)",
        "V?n d?ng v?a (3-5 ngày/tu?n)",
        "V?n d?ng n?ng (6-7 ngày/tu?n)"
    ])
    
    goal = str.selectbox("M?c tiêu hình th?", ["Gi?m cân", "Gi? cân", "Tang co / Tang cân"])
    medical_condition = str.multiselect("Thông tin b?nh lý (n?u có)", ["Ti?u du?ng", "Gout", "Cao huy?t áp"])

# X? lý tính toán ch? s?
activity_factors = {"Ít v?n d?ng (Van phòng)": 1.2, "V?n d?ng nh? (1-3 ngày/tu?n)": 1.375, "V?n d?ng v?a (3-5 ngày/tu?n)": 1.55, "V?n d?ng n?ng (6-7 ngày/tu?n)": 1.725}
r_factor = activity_factors[activity]

if gender == "Nam":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

tdee = bmr * r_factor

if "Gi?m cân" in goal:
    target_cal = tdee - 500
elif "Tang co" in goal:
    target_cal = tdee + 300
else:
    target_cal = tdee

with col2:
    str.header("?? Phân tích & G?i ý th?c don")
    
    # Hi?n th? thông s? t?ng quan
    c1, c2, c3 = str.columns(3)
    c1.metric("Ch? s? BMR (kcal)", f"{bmr:.0f}")
    c2.metric("Ch? s? TDEE (kcal)", f"{tdee:.0f}")
    c3.metric("M?c tiêu Calorie/Ngày", f"{target_cal:.0f} kcal")
    
    str.subheader("??? Món an g?i ý phù h?p v?i b?n")
    
    # Thu?t toán l?c món an thông minh theo m?c tiêu và b?nh lý
    filtered_meals = []
    for meal in MEALS_DB:
        # L?c theo b?nh lý tru?c
        if "Ti?u du?ng" in medical_condition and meal["gi"] == "Cao":
            continue
        if "Gout" in medical_condition and meal["purine"] == "Cao":
            continue
        if "Cao huy?t áp" in medical_condition and meal["sodium"] > 400:
            continue
            
        # L?c theo m?c tiêu hình th? co b?n
        if "Gi?m cân" in goal and meal["calories"] > 500:
            continue
            
        filtered_meals.append(meal)
        
    if not filtered_meals:
        str.warning("Không tìm th?y món an nào phù h?p tuy?t d?i v?i c?u hình b?nh lý ph?c t?p c?a b?n. Vui lòng tham kh?o ý ki?n bác si.")
    else:
        for m in filtered_meals:
            with str.container():
                str.markdown(f"### ?? {m['name']}")
                img_col, info_col = str.columns([1, 2])
                with img_col:
                    if "image" in m:
                        str.image(m["image"], use_column_width=True)
                    else:
                        str.image("https://unsplash.com", use_column_width=True)
                with info_col:
                    str.markdown(f"**?? Nang lu?ng:** `{m['calories']} kcal`")
                    str.markdown(f"*   **Ð?m (Protein):** {m['protein']}g")
                    str.markdown(f"*   **Tinh b?t (Carbs):** {m['carbs']}g")
                    str.markdown(f"*   **Ch?t béo (Fat):** {m['fat']}g")
                    str.markdown(f"*   **Mu?i (Sodium):** {m['sodium']}mg")
                str.divider() 
