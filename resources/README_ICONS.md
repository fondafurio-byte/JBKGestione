# JBK Gestione - Deployment Resources

## Icone necessarie

Per il deployment dell'app sui vari dispositivi, sono necessarie le seguenti icone:

### iOS
- **jbkgestione-1024.png** - 1024x1024px (icona App Store)
- **jbkgestione-180.png** - 180x180px (iPhone)
- **jbkgestione-167.png** - 167x167px (iPad Pro)
- **jbkgestione-152.png** - 152x152px (iPad)
- **jbkgestione-120.png** - 120x120px (iPhone)
- **jbkgestione-87.png** - 87x87px (iPhone 6 Plus)
- **jbkgestione-80.png** - 80x80px (iPad)
- **jbkgestione-76.png** - 76x76px (iPad)
- **jbkgestione-60.png** - 60x60px (iPhone)
- **jbkgestione-58.png** - 58x58px (iPhone)
- **jbkgestione-40.png** - 40x40px (iPad/iPhone)
- **jbkgestione-29.png** - 29x29px (Settings)

### Android
- **jbkgestione-512.png** - 512x512px (Play Store)
- **jbkgestione-192.png** - 192x192px (xxxhdpi)
- **jbkgestione-144.png** - 144x144px (xxhdpi)
- **jbkgestione-96.png** - 96x96px (xhdpi)
- **jbkgestione-72.png** - 72x72px (hdpi)
- **jbkgestione-48.png** - 48x48px (mdpi)
- **jbkgestione-36.png** - 36x36px (ldpi)

### Desktop
- **jbkgestione-256.png** - 256x256px (Windows/Linux)
- **jbkgestione-128.png** - 128x128px (Windows/Linux)
- **jbkgestione-64.png** - 64x64px (Windows/Linux)
- **jbkgestione-32.png** - 32x32px (Windows/Linux)
- **jbkgestione-16.png** - 16x16px (Windows/Linux)

### Web/PWA
- **jbkgestione-192.png** - 192x192px (PWA manifest)
- **jbkgestione-512.png** - 512x512px (PWA manifest)

## Splash Screen
- **jbkgestione-splash-2732x2048.png** - iPad Pro 12.9" landscape
- **jbkgestione-splash-2048x2732.png** - iPad Pro 12.9" portrait
- **jbkgestione-splash-1334x750.png** - iPhone 6/7/8 landscape
- **jbkgestione-splash-750x1334.png** - iPhone 6/7/8 portrait
- **jbkgestione-splash-2208x1242.png** - iPhone 6 Plus landscape
- **jbkgestione-splash-1242x2208.png** - iPhone 6 Plus portrait

## Icona Template (SVG)
L'icona base dovrebbe contenere:
- Logo JBK o simbolo basket
- Colori: Rosso (#dc3545) e bianco
- Design pulito e leggibile anche in piccole dimensioni
- Sfondo trasparente o solido

## Come generare le icone

1. **Manuale**: Crea l'icona base in formato SVG o PNG ad alta risoluzione (1024x1024)
2. **Online**: Usa servizi come AppIcon.co o Icon Generator
3. **Script**: Usa ImageMagick per ridimensionare automaticamente

### Esempio con ImageMagick:
```bash
# Da un'icona base 1024x1024
convert jbkgestione-base.png -resize 180x180 jbkgestione-180.png
convert jbkgestione-base.png -resize 120x120 jbkgestione-120.png
# ... per tutte le dimensioni
```

## Note
- Tutte le icone devono essere in formato PNG
- Sfondo trasparente per iOS, solido per Android
- Respectare le guidelines di design di ogni piattaforma