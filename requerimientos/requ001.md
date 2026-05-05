Análisis Integral para la Implementación de una Plataforma de Salud Digital en el Ecuador: Estrategia Tecnológica, Regulatoria y de Mercado
El ecosistema de salud en la República del Ecuador se encuentra en un punto de inflexión donde la saturación de los servicios públicos y el encarecimiento de la práctica privada convencional han generado una brecha de acceso significativa. Esta coyuntura coincide con una realidad socioprofesional alarmante: la existencia de una vasta cohorte de médicos jóvenes, altamente capacitados, que enfrentan tasas de desempleo o subempleo considerables debido a las barreras de entrada para establecer consultorios físicos propios.1 La propuesta de una plataforma digital fundamentada en Django y PostgreSQL no solo representa una solución tecnológica para la intermediación de servicios médicos, sino que se posiciona como una intervención social y económica capaz de dinamizar el sector salud mediante la democratización de la atención.
El Panorama del Talento Humano y la Salud Digital en Ecuador
La transformación digital de la salud no es meramente una actualización de herramientas, sino un cambio de paradigma en la cadena de valor del sector. En el contexto ecuatoriano, se observa que la telesalud tiene una influencia diferenciada según la especialidad, siendo la psiquiatría, la medicina familiar y la medicina interna las áreas de mayor adopción inicial.2 La oportunidad de empleabilidad para los médicos jóvenes radica en la creación de nuevos roles que trascienden la práctica clínica tradicional, abarcando el apoyo técnico, la gestión de datos de pacientes y la educación sanitaria continua.1
Segmento de Mercado
Necesidad Identificada
Solución Propuesta
Médicos Jóvenes
Falta de capital para consultorio físico y visibilidad.
Plataforma de atención virtual con membresías escalables.
Pacientes
Dificultad de acceso a especialistas y altos costos.
Sistema de solicitud de citas bajo demanda y telemedicina.
Sistema Nacional de Salud
Saturación de hospitales públicos por casos leves.
Triaje y atención primaria digitalizada para reducir carga.

La creación de empleos en el ámbito sanitario no clínico es una tendencia global que el Ecuador puede capitalizar. Se estima que la digitalización requerirá millones de trabajadores adicionales en funciones administrativas, técnicas y de asistencia domiciliaria coordinada digitalmente.1 Por tanto, la plataforma no debe verse solo como un directorio, sino como una infraestructura de servicios que empodera al profesional independiente.
Marco Regulatorio y Cumplimiento Legal en el Ámbito Sanitario
Cualquier emprendimiento tecnológico en salud dentro del territorio ecuatoriano debe navegar por un complejo entramado de resoluciones emitidas por el Ministerio de Salud Pública (MSP) y la Agencia de Aseguramiento de la Calidad de los Servicios de Salud y Medicina Prepagada (ACESS). El cumplimiento normativo no es un valor agregado, sino un requisito de existencia legal que garantiza la seguridad tanto del facultativo como del usuario final.4
Habilitación ante la ACESS y el Permiso de Funcionamiento
La normativa vigente, específicamente el Acuerdo Ministerial 00032-2020 y sus reformas, establece que todos los servicios de atención de salud deben contar obligatoriamente con un permiso de funcionamiento vigente otorgado por la ACESS.4 Para las plataformas digitales que funcionan como establecimientos de salud virtuales, la agencia ha implementado modalidades de inspección virtual para verificar el cumplimiento de los estándares mínimos de calidad.4
La Resolución ACESS-2025-0044-R introduce un sistema de categorización por niveles de riesgo (A, B, C y D), el cual determina la periodicidad de las inspecciones y los requisitos de autoevaluación.5 Para una plataforma que aspira a albergar a miles de médicos, es crítico que cada profesional esté habilitado individualmente, asegurando que su título esté registrado no solo en la SENESCYT, sino también ante la autoridad sanitaria nacional a través de la plataforma de la ACESS.6

Trámite Administrativo
Requisito Principal
Entidad
Registro de Título
Título de 3er o 4to nivel legalizado.
SENESCYT 8
Habilitación Profesional
Certificado de registro en ACESS.
ACESS 6
Permiso de Funcionamiento
RUC activo, infraestructura (física o virtual) validada.
ACESS 4
Registro de Firma Electrónica
Certificado de firma válida para recetas.
Entidades Certificadoras 9

La Ley Orgánica de Protección de Datos Personales (LOPDP)
La salud es una categoría de datos de carácter especial y sensible. En Ecuador, la LOPDP (2021) y su reglamento (2023) imponen obligaciones estrictas sobre el tratamiento de esta información.10 Los artículos 30, 31 y 32 de la ley detallan que el tratamiento de datos de salud debe realizarse exclusivamente por instituciones del Sistema Nacional de Salud o profesionales acreditados, garantizando siempre el secreto profesional y la confidencialidad.12
El diseño de la base de datos PostgreSQL debe contemplar principios de privacidad desde el diseño. Esto implica que, siempre que sea posible, los datos deben ser anonimizados o seudonimizados, especialmente si se planea realizar análisis estadísticos o investigación científica posterior.9 La plataforma debe obtener un consentimiento informado inequívoco de cada paciente, el cual debe ser específico para los fines de telemedicina y almacenamiento de historial clínico.13
Arquitectura del Sistema: Django y PostgreSQL con Restricciones de Recursos
El requerimiento de operar con un límite de 250MB de RAM en el entorno de desarrollo es un desafío técnico que obliga a una optimización profunda y a evitar la sobreingeniería. Django, aunque es un framework robusto, puede ser configurado para mantener una huella de memoria ligera sin sacrificar su capacidad de escalar a miles de usuarios en producción.15
Optimización de PostgreSQL en Entornos de Memoria Limitada
PostgreSQL es extremadamente eficiente, pero su configuración por defecto suele estar pensada para servidores con gigabytes de RAM. Para cumplir con el límite de 250MB, se deben ajustar los parámetros en el archivo postgresql.conf para evitar que el proceso de la base de datos consuma la totalidad de los recursos disponibles.17
Se recomienda la siguiente configuración para el entorno de desarrollo:
shared_buffers: Limitar a 32MB o 64MB para asegurar que el sistema operativo y el proceso de Django tengan espacio suficiente.17
work_mem: Reducir a 2MB o 4MB para evitar que operaciones de ordenamiento complejas agoten la memoria por cada conexión.18
max_connections: Mantener un número bajo de conexiones (por ejemplo, 10 a 20) para reducir la sobrecarga de memoria por cada proceso de backend de la base de datos.17

Parámetro de Memoria
Valor para 250MB (Dev)
Valor para Producción (Escalable)
shared_buffers
32MB
25% de la RAM total 17
work_mem
2MB
64MB o basado en complejidad de queries 19
maintenance_work_mem
16MB
10% de la RAM hasta 1GB 18
temp_buffers
4MB
8MB (Default) 18

Para la gestión de conexiones en producción, es imperativo el uso de un pooler de conexiones como PgBouncer, lo que permitirá manejar miles de usuarios concurrentes sin que PostgreSQL incremente linealmente su consumo de memoria por cada sesión abierta.17
Estructura de Django y Gestión de QuerySets
Para evitar el desperdicio de memoria, el desarrollo en Django debe centrarse en la eficiencia del ORM. El uso de select_related() para relaciones de clave foránea y prefetch_related() para relaciones de muchos a muchos es vital para mitigar el problema de las consultas N+1, que no solo ralentiza la aplicación sino que consume memoria al instanciar objetos duplicados en el contexto de Python.15
En el archivo settings.py, se deben desactivar todas las aplicaciones e intermediarios (middleware) que no sean estrictamente necesarios para la lógica de negocio. Por ejemplo, si la aplicación no requiere sesiones basadas en base de datos para todas las vistas, se puede optar por mecanismos de autenticación más livianos como JWT para la comunicación con el frontend.15
Diseño de Modelos de Datos para Médicos, Especialidades y Validación
La plataforma requiere una estructura de datos flexible que permita a los médicos tener múltiples especialidades y un sistema de validación de credenciales riguroso. El uso de la clase ManyToManyField de Django es el estándar para relacionar médicos con especialidades médicas reconocidas por la ACESS.22
Validación de Credenciales y Almacenamiento de Documentos
El flujo de registro del médico debe incluir la carga de su hoja de vida y títulos en formato PDF. Django maneja esto mediante el campo FileField, el cual debe integrarse con un sistema de almacenamiento que garantice la integridad y privacidad de los archivos.21 El proceso de validación humana implica que un administrador de la plataforma verifique el número de cédula del médico en el portal de la SENESCYT y confirme que el título registrado corresponda a la especialidad declarada.8

Campo de Modelo
Tipo de Dato
Propósito
senescyt_id
CharField
Identificador único del profesional ante el Estado.8
cv_pdf
FileField
Almacenamiento de la trayectoria profesional.
titulos_pdf
FileField
Evidencia documental para validación manual.
is_verified
BooleanField
Flag controlado por el administrador tras la validación.
specialties
ManyToManyField
Asociación con una o más ramas de la medicina.22

La validación por parte de un tercero es un paso crítico para la seguridad del paciente. El sistema debe bloquear la visibilidad del perfil del médico en los resultados de búsqueda hasta que el estado is_verified sea verdadero.6
Estrategia de Pagos y Modelos de Membresía
Para garantizar la sostenibilidad de la plataforma y facilitar las transacciones entre pacientes y médicos, se requiere la integración de pasarelas de pago locales que soporten tanto pagos únicos como cargos recurrentes para las membresías de los médicos.
Comparativa de Pasarelas de Pago en Ecuador

Pasarela
Comisión por Transacción
Fortalezas
PayPhone
5% + IVA 26
Alta adopción, simplicidad en links de pago y QR.28
Kushki
Variable según volumen 29
Soporte nativo para suscripciones recurrentes y tokenización.30
PlaceToPay
Competitiva
Amplia trayectoria y seguridad bancaria.31

Para los médicos, la plataforma debe ofrecer varios niveles de membresía (Suscripciones). Kushki es particularmente fuerte en este aspecto, permitiendo programar cobros automáticos mensuales mediante su API de suscripciones.30 El médico proporciona los datos de su tarjeta una sola vez; Kushki genera un token seguro y procesa el cargo con la periodicidad elegida (mensual, trimestral o anual), eliminando la necesidad de que la plataforma almacene datos sensibles de tarjetas de crédito.33
Para el pago de las consultas por parte de los pacientes, PayPhone ofrece una solución de baja fricción. El uso de la "API Link" permite generar un enlace de pago único por cada cita solicitada, el cual puede ser enviado por correo o mensaje de texto.26 El paciente paga con su saldo PayPhone o cualquier tarjeta de crédito, y los fondos se acreditan de manera inmediata en la billetera de la plataforma para su posterior liquidación al médico.27
Implementación de Telemedicina y Receta Electrónica
La telemedicina virtual es un pilar de la plataforma. Para mantener el desarrollo liviano, se recomienda el uso de Jitsi Meet a través de su API externa. Jitsi es una solución de código abierto que proporciona videoconferencias cifradas de alta calidad sin los costos prohibitivos por minuto de competidores como Twilio.37
Seguridad y Privacidad en la Videoconsulta
La integración de Jitsi en Django se realiza mediante un script en el frontend que carga el iFrame de la reunión. La plataforma debe generar salas con nombres únicos y aleatorios (UUID) y gestionar tokens de autenticación para asegurar que solo el médico y el paciente autorizados puedan ingresar a la sesión.39 Esto cumple con la "Norma Técnica de Telesalud", que exige que las plataformas garanticen la confidencialidad de la atención virtual.9
La Receta Médica Electrónica en Ecuador
La emisión de recetas digitales está estrictamente regulada por la Resolución ACESS-2023-0030. Una receta válida en Ecuador debe incluir obligatoriamente el nombre genérico del medicamento (DCI), la dosis, frecuencia, duración del tratamiento y, fundamentalmente, la firma electrónica del profesional.7

Elemento de la Receta
Requisito ACESS
Implementación en la Plataforma
Datos del Paciente
Nombre, edad, diagnóstico CIE.40
Extracción automática del perfil del paciente y cita.
Datos del Medicamento
Denominación Común Internacional (Genérico).7
Base de datos precargada de fármacos aprobados.
Firma del Médico
Firma electrónica reconocida.7
Integración con certificados.p12 o firma en la nube.
Vigencia
Máximo 3 días para consulta externa.41
Timestamp y fecha de caducidad impresa en el PDF.

La plataforma debe asegurar que cada receta emitida sea única y que se guarde una copia de respaldo por al menos 5 años, tal como lo exige la normativa para fines de auditoría sanitaria.7
Interfaces de Usuario "Chéveres" y Experiencia de Usuario (UX)
Para lograr interfaces modernas y funcionales sin la pesadez de frameworks como React o Vue, el stack recomendado es Tailwind CSS combinado con Alpine.js. Esta combinación permite una reactividad declarativa y ligera, ideal para mantener el consumo de memoria bajo en el cliente y el servidor.42
Componentes Interactivos con Alpine.js
Alpine.js permite manejar estados simples (como abrir/cerrar modales de citas, mostrar notificaciones en tiempo real o realizar filtrados rápidos de médicos) directamente en el HTML de los templates de Django.43 Al no requerir un proceso de construcción (build step) complejo, el flujo de desarrollo se mantiene ágil.
Las interfaces para pacientes deben centrarse en la facilidad de búsqueda por especialidad, calificación y disponibilidad horaria. Siguiendo el modelo de las redes sociales, el sistema de calificación debe permitir al paciente puntuar la atención recibida mediante estrellas y comentarios, los cuales servirán como métrica de calidad para otros usuarios.2
Sugerencias para el Valor Agregado y Escalabilidad
Para que la plataforma soporte miles de usuarios sin caer en la sobreingeniería, se deben implementar estrategias de escalabilidad horizontal y vertical, así como funcionalidades que incrementen la retención de usuarios.
Integración con WhatsApp Business API
Dado que WhatsApp es la herramienta de comunicación más utilizada en Ecuador, integrar notificaciones automáticas para recordatorios de citas es fundamental. El uso de proveedores como 360dialog permite acceder a la API de WhatsApp con costos fijos por número, evitando las altas tarifas de plataforma de otros intermediarios.46 Los mensajes de utilidad (recordatorios) son gratuitos si se envían dentro de la ventana de servicio al cliente de 24 horas iniciada por el usuario.48
Sugerencias Adicionales de Funcionalidad
Módulo de Educación Sanitaria: Permitir a los médicos publicar artículos o consejos de salud. Esto no solo mejora el posicionamiento SEO de la plataforma, sino que ofrece valor al paciente más allá de la consulta.3
Telemonitoreo de Enfermedades Crónicas: Espacios donde el paciente pueda registrar su presión arterial o niveles de glucosa, permitiendo al médico visualizar tendencias antes de la cita.2
Servicio Amigable para Adolescentes: Implementar protocolos de privacidad específicos para jóvenes, cumpliendo con las guías del MSP para una atención inclusiva y equitativa.50
Segunda Opinión Médica: Facilitar flujos donde un paciente pueda compartir su historial con un segundo especialista dentro de la misma plataforma de manera segura.45
Optimización para el Rendimiento de Alta Concurrencia
Para escalar a "miles y miles de usuarios", la aplicación debe estar preparada para manejar picos de tráfico. El uso de Django con servidores de aplicaciones como Gunicorn, configurado con trabajadores asíncronos si la carga es principalmente de E/S (como en telemedicina), permite una mayor concurrencia en el mismo hardware.51
La gestión de la basura (Garbage Collection) en Python también puede ser ajustada para aplicaciones de alto rendimiento. Ajustar los umbrales de gc.set_threshold puede mejorar los tiempos de respuesta en un 5% al reducir la frecuencia de las pausas para limpieza de memoria.51 Asimismo, el uso de librerías como orjson para la serialización de datos JSON puede acelerar drásticamente los endpoints de la API.51
Conclusiones y Recomendaciones Finales
El desarrollo de una plataforma de salud digital en Ecuador utilizando Django y PostgreSQL es un proyecto técnica y legalmente viable, siempre que se respete el marco regulatorio de la ACESS y la LOPDP. El éxito de la iniciativa dependerá de la rigurosidad en la validación de los profesionales y de la capacidad de ofrecer una experiencia de usuario fluida y segura.

Pilar de Éxito
Acción Clave
Justificación
Legal
Validación manual de títulos SENESCYT y firma electrónica.
Garantiza la seguridad del paciente y cumplimiento ACESS.7
Técnico
Optimización de Postgres y uso de Tailwind/Alpine.
Permite operar con recursos limitados y escala eficientemente.18
Financiero
Mix de Kushki (suscripciones) y PayPhone (consultas).
Maximiza la liquidez y facilita el cobro de membresías.26
Social
Enfoque en médicos jóvenes y telemedicina.
Resuelve un problema de empleo y mejora el acceso a salud.1

Al evitar la sobreingeniería y centrarse en herramientas probadas y eficientes, la plataforma podrá escalar orgánicamente, convirtiéndose en una herramienta indispensable para el profesional médico ecuatoriano moderno y una opción confiable para el paciente que busca calidad y accesibilidad en su atención sanitaria.
Obras citadas
Tres oportunidades para mejorar a la vez la atención de la salud y el empleo juvenil, fecha de acceso: mayo 4, 2026, https://blogs.worldbank.org/es/voices/tres-oportunidades-para-mejorar-la-vez-la-atencion-de-la-salud-y-el-empleo-juvenil
Las 4 mejores empresas y plataformas de telemedicina para los proveedores de atención médica en el 2025 - Sermo, fecha de acceso: mayo 4, 2026, https://www.sermo.com/es/resources/las-4-mejores-empresas-y-plataformas-de-telemedicina-para-los-proveedores-de-atencion-medica-en-el-2025/
BID Lab financia telemedicina en Ecuador para llegar a comunidades rurales desatendidas, fecha de acceso: mayo 4, 2026, https://www.iadb.org/es/noticias/bid-lab-financia-telemedicina-en-ecuador-para-llegar-comunidades-rurales-desatendidas
agencia de aseguramiento de la calidad de los - servicios de salud y medicina prepagada - ACESS, fecha de acceso: mayo 4, 2026, http://www.acess.gob.ec/wp-content/uploads/2021/08/Resoluci%C3%B3n-Nro.-ACESS-2020-0050.pdf
Nueva norma para Permisos de Funcionamiento en Salud Ecuador, fecha de acceso: mayo 4, 2026, https://www.meythalerzambranoabogados.com/post/permisos-funcionamiento-salud-acess-2025
Todos los profesionales de la salud, deben registrar su título en la ACESS, fecha de acceso: mayo 4, 2026, http://www.acess.gob.ec/todos-los-profesionales-de-la-salud-deben-registrar-su-titulo-en-la-acess/
Resolución No. ACESS-2023-0030 Página | 1 AGENCIA DE ASEGURAMIENTO DE LA CALIDAD DE LOS SERVICIOS DE SALUD Y MEDICINA PREPAGAD, fecha de acceso: mayo 4, 2026, http://www.acess.gob.ec/wp-content/uploads/2023/11/Resolucion-No.-ACESS-2023-0030.pdf
Ministerio De Educación, Deporte Y Cultura - MINEDEC, fecha de acceso: mayo 4, 2026, https://www.senescyt.gob.ec/web/guest
Norma-Tecnica-de-Telesalud.pdf - ACESS, fecha de acceso: mayo 4, 2026, http://www.acess.gob.ec/wp-content/uploads/2025/11/Norma-Tecnica-de-Telesalud.pdf
Reglamento – Ley Orgánica de Protección de Datos Personales, fecha de acceso: mayo 4, 2026, https://www.telecomunicaciones.gob.ec/wp-content/uploads/2023/11/Decreto-Ejecutivo-No.-904.pdf
Ley Orgánica de Protección de Datos Personales - Consejo de Comunicación, fecha de acceso: mayo 4, 2026, https://www.consejodecomunicacion.gob.ec/wp-content/uploads/downloads/2021/07/lotaip/Ley%20Org%C3%A1nica%20de%20Protecci%C3%B3n%20de%20Datos%20Personales.pdf
Tratamiento de Datos de Salud Ecuador: Guía Completa LOPDP, fecha de acceso: mayo 4, 2026, https://iurenovum.com/tratamiento-de-datos-de-salud-en-ecuador-lo-que-debes-saber/
LEY ORGÁNICA DE PROTECCIÓN DE DATOS PERSONALES - Procuraduria Universitaria UTPL, fecha de acceso: mayo 4, 2026, https://procuraduria.utpl.edu.ec/sitios/documentos/NormativasPublicas/Ley%20de%20Org%C3%A1nica%20de%20Protecci%C3%B3n%20de%20Datos.pdf
GUIA PARA TRATAMIENTO DE DATOS PERSONALES EN ADMINISTRACION PUBLICA - Gobierno Electrónico, fecha de acceso: mayo 4, 2026, https://www.gobiernoelectronico.gob.ec/wp-content/uploads/2019/11/Gu%C3%ADa-de-protecci%C3%B3n-de-datos-personales.pdf
A Complete Guide to Django Performance Optimization - DEV Community, fecha de acceso: mayo 4, 2026, https://dev.to/eraefi/a-complete-guide-to-django-performance-optimization-4ig3
Reducing Django Memory Usage. Low hanging fruit? - Stack Overflow, fecha de acceso: mayo 4, 2026, https://stackoverflow.com/questions/487224/reducing-django-memory-usage-low-hanging-fruit
PostgreSQL Performance Tuning: Optimize Your Database Server - EDB, fecha de acceso: mayo 4, 2026, https://www.enterprisedb.com/postgres-tutorials/introduction-postgresql-performance-tuning-and-optimization
Architecture and Tuning of Memory in PostgreSQL Databases | Severalnines, fecha de acceso: mayo 4, 2026, https://severalnines.com/blog/architecture-and-tuning-memory-postgresql-databases/
Optimización de PostgreSQL (postgresql.conf): Guía Completa de Ajuste de Rendimiento - CubePath Docs, fecha de acceso: mayo 4, 2026, https://cubepath.com/en/docs/gesti%C3%B3n-de-bases-de-datos/optimizacion-de-postgresql-postgresql-conf
Tuning Your PostgreSQL Server/es, fecha de acceso: mayo 4, 2026, https://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server/es
Django Performance Optimization Tips - TestDriven.io, fecha de acceso: mayo 4, 2026, https://testdriven.io/blog/django-performance-optimization-tips/
Relación muchos a muchos con Django - YouTube, fecha de acceso: mayo 4, 2026, https://www.youtube.com/watch?v=QBzsoQPgJQ8
Relaciones de Muchos a Muchos en Modelos de Base de Datos - Platzi, fecha de acceso: mayo 4, 2026, https://platzi.com/cursos/django/relaciones-uno-a-muchos-1n-en-django/
Tutorial Django Parte 3: Uso de modelos - Aprende desarrollo web | MDN, fecha de acceso: mayo 4, 2026, https://developer.mozilla.org/es/docs/Learn_web_development/Extensions/Server-side/Django/Models
Obtención del reconocimiento general de títulos del extranjero | Ecuador - Gob.EC, fecha de acceso: mayo 4, 2026, https://www.gob.ec/minedec/tramites/obtencion-reconocimiento-general-titulos-extranjero
API Link in Ecuador: Automate Payment Link Generation - Payphone, fecha de acceso: mayo 4, 2026, https://payphone.app/en-ec/solutions/api-link
Payphone: Aceptar pagos con tarjeta sin datáfono en Ecuador, fecha de acceso: mayo 4, 2026, https://payphone.app/
API para links de pago en Ecuador (cobros automáticos) - Payphone, fecha de acceso: mayo 4, 2026, https://payphone.app/soluciones/api-link
Tarifas Kushki | Precios Competitivos para Procesar Pagos, fecha de acceso: mayo 4, 2026, https://www.kushkipagos.com/tarifas-comisiones
Create a recurring charge | 1. Online Payments - Kushki API, fecha de acceso: mayo 4, 2026, https://api-docs.kushkipagos.com/docs/online-payments/one-click-and-scheduled-payments/operations/create-a-subscription-v-1-card
5 pasarelas o botones de pago en Ecuador ¿Cuál te conviene?, fecha de acceso: mayo 4, 2026, https://serendipia.ec/pasarelas-botones-de-pago-ecuador/
Create a recurring charge | Kushki Docs, fecha de acceso: mayo 4, 2026, https://docs.kushki.com/ec/recurring-payments/scheduled-payments/subscribe-a-card/
Schedule a recurring charge | Kushki Docs, fecha de acceso: mayo 4, 2026, https://docs.kushki.com/co/en/recurring-payments/scheduled-payments/subscribe-a-card/
API Kushki | Stoplight, fecha de acceso: mayo 4, 2026, https://api-docs.kushkipagos.com/
Payment Solutions for Businesses in Ecuador | Payphone, fecha de acceso: mayo 4, 2026, https://payphone.app/en-ec/payment-solutions
API Sale en Ecuador: cobros por solicitud desde app - Payphone, fecha de acceso: mayo 4, 2026, https://payphone.app/soluciones/api-sale
Twilio vs Jitsi: Choosing the Appropriate Solution - Video SDK - VideoSDK, fecha de acceso: mayo 4, 2026, https://www.videosdk.live/twilio-vs-jitsi
Jitsi vs Twilio: Which Video Platform Is Right for You? - Jitsi Guide, fecha de acceso: mayo 4, 2026, https://jitsi.guide/blog/jitsi-vs-twilio/
The Best Video Call API and SDK Platforms | Whereby, fecha de acceso: mayo 4, 2026, https://whereby.com/blog/best-video-call-api-and-sdk-platforms/
Página 1 de 18 AGENCIA DE ASEGURAMIENTO DE LA CALIDAD DE LOS SERVICIOS DE SALUD Y MEDICINA PREPAGADA – ACESS RESOLUCIÓN No., fecha de acceso: mayo 4, 2026, http://www.acess.gob.ec/wp-content/uploads/2021/08/Resoluci%C3%B3n-Nro.-ACESS-2021-0006.pdf
Reglamento para recetas en Ecuador 2026: qué debe tener tu receta para evitar multas de ACESS - Doctocliq, fecha de acceso: mayo 4, 2026, https://www.doctocliq.com/blog/reglamento-recetas-ecuador-2026
27 Best Tailwind CSS Admin Dashboard Templates (2026) - Colorlib, fecha de acceso: mayo 4, 2026, https://colorlib.com/wp/tailwind-admin-dashboard-templates/
Using Alpine.js in Django: A Lightweight Alternative to Heavy Frontend Frameworks, fecha de acceso: mayo 4, 2026, https://wawaziphil.medium.com/using-alpine-js-in-django-a-lightweight-alternative-to-heavy-frontend-frameworks-feeb15c3bc20
ReThinking Django Template: Part 1 - SaaS Hammer, fecha de acceso: mayo 4, 2026, https://saashammer.com/blog/rethinking-django-template-part-1/
Las Plataformas de Telemedicina Más Eficientes en Ecuador - Anuario LATAM seguros, fecha de acceso: mayo 4, 2026, https://anuariolatamseguros.com/blog/salud/las-plataformas-de-telemedicina-mas-eficientes-en-ecuador/
Twilio vs. 360 Dialog: Which WhatsApp API Provider Is Best for Your Business?, fecha de acceso: mayo 4, 2026, https://www.kommunicate.io/blog/twilio-vs-360dialog-a-comparison/
Top WhatsApp Business API Providers Compared (2026) | Kanal, fecha de acceso: mayo 4, 2026, https://getkanal.com/blog/whatsapp-business-api-providers-compared
WhatsApp Messaging Pricing - Twilio, fecha de acceso: mayo 4, 2026, https://www.twilio.com/en-us/whatsapp/pricing
Pricing on the WhatsApp Business Platform - Meta for Developers, fecha de acceso: mayo 4, 2026, https://developers.facebook.com/docs/whatsapp/pricing/
¿Qué es un servicio amigable para adolescentes? - Ministerio de Salud Pública, fecha de acceso: mayo 4, 2026, https://www.salud.gob.ec/que-es-un-servicio-amigable-para-adolescentes/
Optimizing Django for High Traffic: A Practical Guide to Boosting Performance, fecha de acceso: mayo 4, 2026, https://meamka.me/posts/practical-guide-to-optimizing-django-for-high-traffic/
I Fixed My Slow Nginx + Gunicorn Setup — Here's How It Became 3X Faster - DevOps.dev, fecha de acceso: mayo 4, 2026, https://blog.devops.dev/i-fixed-my-slow-nginx-gunicorn-setup-heres-how-it-became-3x-faster-1c324eb9bbb5

la idea es que la plataforma sirva como intermediario pero con responsabilidad minima que la plataforma cobre mensual a los medicos y podria ser a los pacientes se podria incorporar ia para buscar de acuerdo a la hoja de vida al medico mas apto.

se debe trabajar con docker-compose
