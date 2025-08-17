# Respira y Relájate - Skill de Alexa

## 📖 Descripción

**Respira y Relájate** es una skill de Amazon Alexa diseñada para ayudar a los usuarios a gestionar el estrés y mejorar su bienestar emocional a través de ejercicios guiados de respiración y mindfulness. La aplicación incluye evaluaciones personalizadas que recomiendan actividades específicas según el estado emocional del usuario.

## ✨ Características Principales

### 🧘‍♀️ Ejercicios de Respiración
- **Respiración Básica**: Ejercicio fundamental con ciclos personalizables (inhalar-mantener-exhalar)
- **Técnica 4-7-8**: Método especializado para la relajación profunda
- **Respiración en Caja (Box Breathing)**: Técnica de respiración cuadrada para el enfoque y concentración

### 🧠 Ejercicios de Mindfulness
- **Escaneo Corporal**: Guía para conectar con el cuerpo y liberar tensiones
- **Atención Plena**: Ejercicios de observación consciente del entorno
- **Gratitud**: Reflexiones guiadas para fomentar pensamientos positivos

### 📊 Evaluaciones Personalizadas
- **Test de Estrés**: Evalúa el nivel de estrés actual del usuario
- **Test de Bienestar Emocional**: Mide el estado de bienestar general
- **Recomendaciones Automáticas**: Sugiere ejercicios específicos basados en los resultados

### 🎵 Ambiente Relajante
- Música de fondo relajante que se reproduce automáticamente
- Rotación continua entre diferentes pistas ambientales
- Sonidos de la naturaleza y música instrumental

## 🚀 Instalación y Configuración

### Prerrequisitos
- Amazon Developer Console account
- AWS account con permisos para Lambda y DynamoDB
- ASK CLI (Alexa Skills Kit Command Line Interface)

### Configuración del Proyecto

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/EdJGM/SkillAlexa.git
   cd SkillAlexa
   ```

2. **Configurar las credenciales**
   ```bash
   ask configure
   ```

3. **Instalar dependencias**
   ```bash
   cd lambda
   pip install -r requirements.txt
   ```

4. **Desplegar la skill**
   ```bash
   ask deploy
   ```

## 🏗️ Estructura del Proyecto

```
Respirayrelajate/
├── skill-package/
│   ├── skill.json                     # Configuración de la skill
│   └── interactionModels/
│       └── custom/
│           └── es-MX.json            # Modelo de interacción en español
├── lambda/
│   ├── lambda_function.py            # Lógica principal de la skill
│   ├── utils.py                      # Utilidades auxiliares
│   └── requirements.txt              # Dependencias de Python
├── public/
│   └── mindfulness_11157253.png      # Recursos gráficos
├── ask-resources.json                # Configuración del ASK CLI
└── *.mp3                            # Archivos de música ambiente
```

## 🎮 Uso de la Skill

### Activación
```
"Alexa, abre Respira y Relájate"
```

### Comandos Principales

#### Tests de Evaluación
- "Quiero hacer el test de estrés"
- "Test de bienestar emocional"

#### Ejercicios de Respiración
- "Ejercicio básico"
- "Respiración cuatro siete ocho"
- "Respiración en caja"
- "Ejercicio básico con 8 ciclos"

#### Ejercicios de Mindfulness
- "Escaneo corporal"
- "Atención plena"
- "Ejercicio de gratitud"

#### Navegación
- "Menú principal"
- "Regresar al menú"
- "Ayuda"

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje de programación principal
- **ASK SDK for Python**: Framework para el desarrollo de skills de Alexa
- **AWS Lambda**: Servicio de computación serverless
- **Amazon DynamoDB**: Base de datos NoSQL para persistencia
- **boto3**: SDK de AWS para Python

## 📦 Dependencias

```python
boto3==1.28.78
ask-sdk-core==1.19.0
```

## 🔧 Configuración Avanzada

### Variables de Entorno
La skill utiliza las siguientes variables de entorno:
- `DYNAMODB_PERSISTENCE_REGION`: Región de DynamoDB
- `DYNAMODB_PERSISTENCE_TABLE_NAME`: Nombre de la tabla
- `S3_PERSISTENCE_REGION`: Región de S3 (para archivos multimedia)
- `S3_PERSISTENCE_BUCKET`: Bucket de S3

### Base de Datos
La aplicación almacena:
- Historial de tests realizados
- Respuestas de evaluaciones
- Preferencias del usuario
- Métricas de uso

## 🌍 Idiomas Soportados

Actualmente la skill está disponible en:
- **Español (México)** - es-MX

## 🎯 Funcionalidades Futuras

- [ ] Soporte para más idiomas
- [ ] Recordatorios personalizados
- [ ] Estadísticas de progreso
- [ ] Integración con dispositivos wearables
- [ ] Más ejercicios de mindfulness
- [ ] Modo offline

## 👥 Contribución

1. Fork el proyecto
2. Crea tu rama de funcionalidad (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**EdJGM** - [GitHub](https://github.com/EdJGM)

## 🙏 Agradecimientos

- Amazon Alexa Developer Program
- Recursos de audio de Freesound.org
- Comunidad de desarrolladores de Alexa Skills

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:
1. Revisa los [Issues](https://github.com/EdJGM/SkillAlexa/issues) existentes
2. Crea un nuevo issue si es necesario
3. Consulta la documentación oficial de Alexa Skills Kit

---

*"Respira profundo, relájate y encuentra tu equilibrio interior con Alexa"* 🧘‍♀️✨
