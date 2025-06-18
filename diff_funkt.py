import streamlit as st
import sympy as sp
import random

# Opsætning
st.set_page_config(page_title="Differentieringstræning", layout="centered")

st.title("📘 Træn differentiering – STX A/B")

x = sp.symbols('x')

# Funktion til pæn LaTeX med ln i stedet for log
def latex_med_ln(expr):
    latex_str = sp.latex(expr)
    latex_str = latex_str.replace(r'\log', r'\ln')
    return latex_str

# SIDEBAR
with st.sidebar:
    st.header("ℹ️ Hjælp og info")

    with st.expander("📘 Notationshjælp – hvordan du skriver funktioner"):
        st.markdown(r"$x^2$ — skriv: `x**2`")
        st.markdown(r"$3x$ — skriv: `3*x`")
        st.markdown(r"$\sin(x)$ — skriv: `sin(x)`")
        st.markdown(r"$\cos(x)$ — skriv: `cos(x)`")
        st.markdown(r"$e^x$ — skriv: `exp(x)`")
        st.markdown(r"$a^x$ — skriv: `a**x` (fx `2**x` for 2 i eksponenten)")
        st.markdown(r"$\ln(x)$ — skriv: `ln(x)` (brug **ln**, ikke log)")
        st.markdown(r"$\frac{1}{x}$ — skriv: `1/x`")
        st.markdown(r"$\sqrt{x}$ — skriv: `x**(1/2)`")

    st.subheader("🧪 Test notation")

    st.markdown("**Prøv at skrive en funktion med den specielle notation.**")
    st.markdown("Eksempler på funktioner du kan prøve at skrive:")

    st.latex(r"f(x) = \sin(3x + 1)")
    st.latex(r"f(x) = e^{x^2}")
    st.latex(r"f(x) = \ln(5x)")

    test_input = st.text_input("Skriv en funktion (fx sin(2*x))")

    if test_input:
        try:
            test_expr = sp.sympify(test_input.replace("ln(", "log("))
            st.latex(f"f(x) = {latex_med_ln(test_expr)}")
        except Exception:
            st.error("⚠️ Kunne ikke tolkes. Tjek *, parenteser osv.")

    st.markdown("---")
    st.markdown("""
**📄 Licens:** MIT  
**👨‍💻 Udvikler:** Dit Navn  
**🤖 Med hjælp fra:** ChatGPT (OpenAI)
""")

# Funktion til at generere funktioner
def generer_funktion():
    a = random.randint(2, 5)  # basetal for a^x
    b = random.randint(-5, 5)
    indre = a * x + b

    typer = [
        lambda: x**random.randint(2, 5),            # potensfunktion
        lambda: a * x**random.randint(1, 3),        # lineær kombination af potens
        lambda: sp.sin(indre),                       # sin(a*x + b)
        lambda: sp.cos(indre),                       # cos(a*x + b)
        lambda: sp.exp(indre),                       # e^(a*x + b)
        lambda: sp.log(indre),                       # ln(a*x + b)
        lambda: sp.exp(x**2 + b * x),                # e^(x^2 + b*x)
        lambda: a**x,                                # a^x
        lambda: 1/x,                                 # 1/x
        lambda: x**(sp.Rational(1, 2)),             # sqrt(x)
    ]
    return random.choice(typer)()

# Ny opgave og nulstil svar
if 'funktion' not in st.session_state or st.button("🔁 Ny opgave"):
    st.session_state.funktion = generer_funktion()
    st.session_state.svar = ""  # Nulstil inputfelt

funktion = st.session_state.funktion
korrekt_afledt = sp.diff(funktion, x)

# Vis opgave
st.latex(f"f(x) = {latex_med_ln(funktion)}")
elev_svar = st.text_input("👉 Skriv f'(x):", key="svar")

# Evaluering
if elev_svar:
    try:
        elev_svar_forbehandlet = elev_svar.replace("ln(", "log(")
        elev_afledt = sp.sympify(elev_svar_forbehandlet)
        korrekt = sp.simplify(elev_afledt - korrekt_afledt) == 0

        st.write("🧠 Dit svar:")
        st.latex(f"f'(x) = {latex_med_ln(elev_afledt)}")

        if korrekt:
            st.success("✅ Korrekt!")
        else:
            st.error("❌ Det er ikke korrekt.")
            if st.checkbox("📖 Vis facit"):
                st.latex(f"f'(x) = {latex_med_ln(korrekt_afledt)}")

    except Exception as e:
        st.error(f"⚠️ Der er en fejl i dit input: {e}")
