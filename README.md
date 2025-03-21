# Pilotes macOS pour le nouveau clavier AZERTY normalisé

Utilisez votre clavier existant pour tester la nouvelle disposition des symboles. Vous pouvez l’apprendre en vous aidant du clavier virtuel de macOS ou du site <https://norme-azerty.fr>.

Une transcription de la norme NF Z 71‐300 A est utilisée pour générer le pilote: [kbdrefs/nf_z71_300.md](kbdrefs/nf_z71_300.md).

## Installation

Pour utiliser un nouveau clavier externe :

- Brancher le clavier avant d’installer le pilote.
- Vérifier que le type de clavier détecté est bien européen « ISO/IEC 9995 ».
- Si ce n’est pas le cas, revenir à l’étape précédente. Au moment d’appuyer sur la touche à côté de Shift, appuyer sur une ou plusieurs autres touches jusqu’à ce que l’assistant vous informe qu’il ne parvient pas à détecter le type de clavier. Choisir le clavier européen « ISO/IEC 9995 ».

![Keyboard Setup Assistant ISO/IEC 9995](https://cyril.lugan.fr/assets/misc/fix-mac-inverted-keys/select-iso-keyboard.png)

Pour installer le pilote :

- Télécharger le dernier pilote publié sur la page [Releases](https://github.com/cyril-L/normalized-azerty/releases)
- Décompresser le fichier `.zip`
- Déplacer le fichier `French NF.bundle` dans la bibliothèque :
  - Depuis le *Finder* → `Aller` → `Aller au dossier`
  - Pour installer le pilote uniquement pour votre utilisateur, entrez `~/Library/Keyboard Layouts`
  - Pour installer le pilote pour tous les utilisateurs, entrez `/Library/Keyboard Layouts` (vous devez disposer des droits d’administration)
  - Déplacer le fichier `French NF.bundle` dans le dossier `Keyboard Layouts`
- Activer la disposition depuis les *Préférences Système* → `Clavier` → `Méthodes et saisie` → `+` → `Français normalisé (AZERTY)`
- Redémarrer la session

## Mise à jour

Pour mettre à jour le pilote, remplacer le fichier `.bundle` existant et redémarrer la session.

## Touches @ et &lt; inversées

Si les touches <kbd>@</kbd> et <kbd>&lt;</kbd> sont inversées, il est possible que macOS n’ai pas correctement identifié le clavier.

Voir [Issue #9](https://github.com/cyril-L/normalized-azerty/issues/9) ou [Fix inverted keys on a Mac](https://cyril.lugan.fr/misc/fix-mac-inverted-keys.html).

## Build

Pour faire une nouvelle release:

- Générer le fichier [French - NF.keylayout](https://github.com/cyril-L/normalized-azerty/blob/master/French%20NF.bundle/Contents/Resources/French%20-%20NF.keylayout). Ce fichier est également versionné, il est possible de le modifier avec le logiciel [Ukelele](http://scripts.sil.org/ukelele).
  ```
  ./make_macos_keylayout.py > French\ NF.bundle/Contents/Resources/French\ -\ NF.keylayout
  ```
- Mettre à jour le fichier [Info.plist](https://github.com/cyril-L/normalized-azerty/blob/master/French%20NF.bundle/Contents/Info.plist) manuellement.
- Compresser `French NF.bundle`
  ```
  zip -r normalized-azerty-v0.0.7.zip French\ NF.bundle/
  ```

## Contribution

- Rapportez un problème ou une suggestion sur la page [Issues](https://github.com/cyril-L/normalized-azerty/issues)
- La disposition suit la description présentée sur le site <https://norme-azerty.fr>.
- Les caractères Unicode ont principalement été récupérés sur :
  - <https://bepo.fr/wiki/Touches_mortes>
  - <https://github.com/marcbal/Printable-AZERTY-NF>
- Des informations sur le format du fichier `.keylayout` sont disponibles sur [Technical Note TN2056 - Installable Keyboard Layouts](https://developer.apple.com/library/archive/technotes/tn2056/_index.html)