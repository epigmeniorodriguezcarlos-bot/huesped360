# app.py - Huésped 360 (Enterprise Edition)
import datetime
import os
import sqlite3
import streamlit as st

# Intentar importar google.generativeai
try:
  import google.generativeai as genai

  HAS_GEMINI = True
except ImportError:
  HAS_GEMINI = False

# Configuración de la página
st.set_page_config(
    page_title="Huésped 360 | Plataforma Hotelera Inteligente",
    page_icon="🏨",
    layout="wide",
)

# Inicialización de Base de Datos SQLite local (100% gratis y sin servidores externos)


def init_db():
  conn = sqlite3.connect("huesped360.db")
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            room TEXT,
            check_in TEXT,
            check_out TEXT,
            preferences TEXT,
            status TEXT
        )
    """)
  conn.commit()
  conn.close()


init_db()

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-header { font-size: 2.3rem; color: #1E3A8A; font-weight: 700; }
    .sub-header { font-size: 1.1rem; color: #4B5563; }
    .card { background-color: #F9FAFB; padding: 20px; border-radius: 10px; border: 1px solid #E5E7EB; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# Sidebar de Navegación
st.sidebar.image(
    "https://img.icons8.com/color/96/hotel-check-in.png", width=70
)
st.sidebar.title("Huésped 360 🏨")
st.sidebar.markdown(
    "*Plataforma de Experiencia y Operaciones Hoteleras*"
)

menu = st.sidebar.selectbox(
    "Menú Principal", [
        "📊 Dashboard Gerencial",
        "👥 CRM de Huéspedes",
        "🤖 Conserje IA (Gemini)",
        "⭐ Análisis de Satisfacción",
        "🚀 Cómo Presentarlo",
    ]
)

# Configuración de API Key de Gemini en el sidebar
st.sidebar.markdown("---")
api_key = st.sidebar.text_input(
    "🔑 Google Gemini API Key",
    type="password",
    help="Introduce tu API Key gratuita de Google AI Studio",
)

if api_key and HAS_GEMINI:
  genai.configure(api_key=api_key)

# ----------------- 1. DASHBOARD GERENCIAL -----------------
if menu == "📊 Dashboard Gerencial":
  st.markdown(
      '<p class="main-header">📊 Dashboard Operativo en Tiempo Real</p>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<p class="sub-header">Métricas clave para la toma de decisiones'
      " gerenciales.</p>",
      unsafe_allow_html=True,
  )

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric(
        label="🛏️ Ocupación Hotelera", value="88%", delta="+4% vs ayer"
    )
  with col2:
    st.metric(label="👥 Huéspedes Activos", value="142", delta="+12 nuevos")
  with col3:
    st.metric(label="⭐ Satisfacción (CSAT)", value="4.8 / 5.0", delta="+0.2")
  with col4:
    st.metric(
        label="🤖 Consultas IA Atendidas", value="340", delta="98% éxito"
    )

  st.markdown("---")
  c1, c2 = st.columns(2)
  with c1:
    st.subheader("🛎️ Solicitudes Activas de Habitaciones")
    st.info(
        "Habitación 302: Solicitud de almohadas adicionales (Completado)"
    )
    st.success(
        "Habitación 105: Reserva de tour gastronómico local (Confirmado)"
    )
    st.warning(
        "Habitación 412: Reporte de asistencia técnica A/C (En proceso)"
    )

  with c2:
    st.subheader("💡 Insights de Negocio generados por IA")
    st.markdown("""
        - 📈 **Alta demanda en tours**: El 65% de los huéspedes recientes consultan por experiencias cafeteras y gastronómicas.
        - 💰 **Oportunidad de Upsell**: 34 solicitudes de *late check-out* registradas esta semana.
        - 🌟 **Punto fuerte**: El servicio de recepción mantiene la calificación más alta del trimestre.
        """)

# ----------------- 2. CRM DE HUÉSPEDES -----------------
elif menu == "👥 CRM de Huéspedes":
  st.markdown(
      '<p class="main-header">👥 CRM & Perfil 360 del Huésped</p>',
      unsafe_allow_html=True,
  )

  conn = sqlite3.connect("huesped360.db")
  cursor = conn.cursor()

  with st.expander("➕ Registrar Nuevo Huésped / Estancia"):
    with st.form("guest_form"):
      g_name = st.text_input("Nombre Completo del Huésped")
      g_email = st.text_input("Correo Electrónico")
      g_room = st.text_input("Número de Habitación")
      g_in = st.date_input("Fecha de Check-in", datetime.date.today())
      g_out = st.date_input(
          "Fecha de Check-out",
          datetime.date.today() + datetime.timedelta(days=3),
      )
      g_pref = st.text_area(
          "Preferencias o Alergias (Ej: Alérgico al marisco, prefiere planta"
          " alta)"
      )
      submitted = st.form_submit_button("Guardar en Base de Datos")
      if submitted and g_name:
        cursor.execute(
            "INSERT INTO guests (name, email, room, check_in, check_out,"
            " preferences, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                g_name,
                g_email,
                g_room,
                str(g_in),
                str(g_out),
                g_pref,
                "Activo",
            ),
        )
        conn.commit()
        st.success(f"¡Huésped {g_name} registrado correctamente!")

  st.subheader("📋 Directorio de Huéspedes Actuales")
  cursor.execute(
      "SELECT name, email, room, check_in, check_out, preferences FROM guests"
  )
  guests = cursor.fetchall()
  conn.close()

  if guests:
    for g in guests:
      st.markdown(f"""
            <div class="card">
                <h4>🏨 {g[0]} — Habitación {g[2]}</h4>
                <p><b>📧 Email:</b> {g[1]} | <b>📅 Estancia:</b> {g[3]} al {g[4]}</p>
                <p><b>⭐ Preferencias y Notas:</b> {g[5]}</p>
            </div>
            """, unsafe_allow_html=True)
  else:
    st.info(
        "Aún no hay huéspedes registrados. Añade uno usando el formulario de"
        " arriba."
    )

# ----------------- 3. CONSERJE IA (GEMINI) -----------------
elif menu == "🤖 Conserje IA (Gemini)":
  st.markdown(
      '<p class="main-header">🤖 Conserje Virtual Inteligente</p>',
      unsafe_allow_html=True,
  )
  st.markdown(
      "Asistente virtual entrenado para responder automáticamente las 24 horas"
      " sobre servicios, políticas y recomendaciones locales."
  )

  if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "¡Hola! Soy el conserje virtual de Huésped 360. ¿En qué puedo"
            " ayudarte con tu estancia o servicios del hotel?"
        ),
    }]

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if prompt := st.chat_input(
      "Pregunta algo (Ej: ¿A qué hora abre el desayuno? ¿Qué lugares me"
      " recomiendan visitar?)..."
  ):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    with st.chat_message("assistant"):
      with st.spinner("Consultando base de conocimientos del hotel..."):
        if api_key and HAS_GEMINI:
          try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            context = (
                "Eres el conserje virtual del hotel boutique Huésped 360."
                " Respondes de forma amable y ejecutiva. Datos clave:"
                " Desayuno: 7:00 AM - 10:30 AM en el restaurante principal."
                " Check-out: 12:00 PM. Wi-Fi gratuito: Red 'Huesped360_Guest',"
                " sin contraseña. Recepción y seguridad 24/7."
            )
            response = model.generate_content(
                f"{context}\n\nPregunta del huésped: {prompt}"
            )
            answer = response.text
          except Exception as e:
            answer = f"Error al conectar con la API de Gemini: {e}"
        else:
          # Respuesta simulada inteligente si no se ha introducido la API Key
          answer = (
              f"[Modo Demo sin API Key]: Entiendo tu consulta sobre '{prompt}'."
              " En Huésped 360 nuestro desayuno es de 7:00 a 10:30 AM y el Wi-Fi"
              " es gratuito. *Tip: Ingresa tu Google Gemini API Key gratuita en"
              " el menú lateral para activar el modelo de lenguaje en vivo.*"
          )
        st.markdown(answer)
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

# ----------------- 4. ANÁLISIS DE SATISFACCIÓN -----------------
elif menu == "⭐ Análisis de Satisfacción":
  st.markdown(
      '<p class="main-header">⭐ Análisis de Reseñas y Comentarios</p>',
      unsafe_allow_html=True,
  )

  col1, col2 = st.columns(2)
  with col1:
    st.subheader("📝 Registrar Comentario de Huésped")
    with st.form("review_form"):
      r_name = st.text_input("Nombre del Huésped")
      r_rating = st.slider("Calificación", 1, 5, 5)
      r_comment = st.text_input("Comentario")
      r_submit = st.form_submit_button("Evaluar Sentimiento")
      if r_submit:
        sentimiento = (
            "Positivo 🟢"
            if r_rating >= 4
            else ("Neutral 🟡" if r_rating == 3 else "Negativo 🔴")
        )
        st.success(
            f"Reseña procesada con éxito. Sentimiento detectado: {sentimiento}"
        )

  with col2:
    st.subheader("📊 Resumen de Satisfacción Semanal")
    st.markdown("""
        - 🟢 **Comentarios Positivos (78%)**: Destacan la amabilidad del personal y la comodidad de las habitaciones.
        - 🟡 **Neutrales (15%)**: Solicitan mayor variedad de opciones en el room service nocturno.
        - 🔴 **Negativos (7%)**: Demora puntual en el proceso de entrega de llaves durante el fin de semana.
        """)

# ----------------- 5. CÓMO PRESENTARLO -----------------
elif menu == "🚀 Cómo Presentarlo":
  st.markdown(
      '<p class="main-header">🚀 Guía de Pitch para la Empresa</p>',
      unsafe_allow_html=True,
  )
  st.markdown("""
    ### Estructura recomendada para tu presentación comercial:
    
    1. **El Gancho (Problema):** *"Los hoteles pierden tiempo valiente respondiendo las mismas preguntas en recepción (horarios, Wi-Fi, ubicación) y carecen de un CRM ágil y económico."*
    2. **La Solución (Huésped 360):** *"Presento Huésped 360, una plataforma inteligente que unifica la gestión de huéspedes, análisis de satisfacción y un conserje virtual con Inteligencia Artificial."*
    3. **Demostración en Vivo:**
       - Muestra el **Dashboard** para que vean el control operativo.
       - Añade un huésped en el **CRM**.
       - Hazle una pregunta difícil al **Conserje IA** para demostrar la velocidad de respuesta.
    4. **El Beneficio Financiero (Costo Cero / Open Source):** Explica que la app está construida con tecnologías modernas y gratuitas, lo que elimina costosas tarifas de licencias de software tradicional.
    """)
