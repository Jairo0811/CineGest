# Seguridad de CineGest

## Versiones soportadas

CineGest se mantiene como proyecto académico/profesional de portafolio. Después de la publicación de `v1.0.0`, las correcciones de seguridad se aplicarán sobre la rama `main` y, cuando corresponda, mediante versiones de parche `1.0.x`.

## Reporte de vulnerabilidades

No publiques secretos, credenciales, datos personales reales ni detalles explotables en issues públicos.

Si detectas una vulnerabilidad en una instalación propia de CineGest:

1. confirma que utilizas una versión actualizada de `main` o del último release;
2. reproduce el problema con datos ficticios;
3. documenta componente afectado, impacto y pasos mínimos de reproducción;
4. evita incluir contraseñas, claves privadas, cadenas de conexión o bases de datos reales.

## Requisitos mínimos de producción

Una instalación de producción debe cumplir, como mínimo:

- `DJANGO_DEBUG=False`;
- `DJANGO_SECRET_KEY` aleatorio, exclusivo del entorno y de al menos 32 caracteres;
- `DJANGO_ALLOWED_HOSTS` limitado a hosts válidos;
- `DJANGO_CSRF_TRUSTED_ORIGINS` configurado para los orígenes HTTPS utilizados;
- HTTPS habilitado mediante reverse proxy o balanceador;
- SQL Server no expuesto directamente a Internet;
- copias de seguridad periódicas y verificadas;
- rotación de credenciales;
- dependencias e imágenes Docker mantenidas al día.

CineGest bloquea el arranque con `DJANGO_DEBUG=False` cuando detecta una clave secreta de desarrollo o una lista vacía de hosts permitidos.

## Datos de prueba

La suite automatizada utiliza exclusivamente datos ficticios. No deben incorporarse cédulas, nombres, correos, teléfonos o credenciales de personas reales en fixtures, pruebas, capturas o documentación pública.
