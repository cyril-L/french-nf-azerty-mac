# Pilotes macOS pour le nouveau clavier AZERTY normalisé

Utilisez votre clavier existant pour tester la nouvelle disposition des symboles. Vous pouvez l’apprendre en vous aidant du clavier virtuel de macOS ou du site <https://norme-azerty.fr>.

## Installation

- Téléchargez le dernier pilote publié sur la page [Releases](https://github.com/cyril-L/normalized-azerty/releases)
- Décompressez le fichier `.zip`
- Déplacez le fichier `French NF.bundle` dans la bibliothèque :
  - Depuis le *Finder* → `Aller` → `Aller au dossier`
  - Pour installer le pilote uniquement pour votre utilisateur, entrez `~/Library/Keyboard Layouts`
  - Pour installer le pilote pour tous les utilisateurs, entrez `/Library/Keyboard Layouts` (vous devez disposer des droits d’administration)
  - Déplacez le fichier `French NF.bundle` dans le dossier `Keyboard Layouts`
- Activez la disposition depuis les *Préférences Système* → `Clavier` → `Méthodes et saisie` → `+` → `French - NF`
- Redémarrez votre session


## Mise à jour

Pour mettre à jour le pilote, remplacez le fichier `.bundle` existant et redémarrez votre session.

## Touches @ et &lt; inversées

Si les touches <kbd>@</kbd> et <kbd>&lt;</kbd> sont inversées, il est possible que macOS n’ai pas correctement identifié le clavier.

Voir [Fix inverted keys on a Mac](https://cyril.lugan.fr/misc/fix-mac-inverted-keys.html).

## Contribution

Un script Python est utilisé pour générer le fichier [French - NF.keylayout](https://github.com/cyril-L/normalized-azerty/blob/master/French%20NF.bundle/Contents/Resources/French%20-%20NF.keylayout):

```
./make_macos_keylayout.py > French\ NF.bundle/Contents/Resources/French\ -\ NF.keylayout
```

Ce fichier généré est également versionné dans ce dépot, il est possible de le modifier avec le logiciel [Ukelele](http://scripts.sil.org/ukelele).

- Rapportez un problème ou une suggestion sur la page [Issues](https://github.com/cyril-L/normalized-azerty/issues)
- La disposition suit la description présentée sur le site <https://norme-azerty.fr>.
- Les caractères Unicode ont principalement été récupérés sur :
  - <https://bepo.fr/wiki/Touches_mortes>
  - <https://github.com/marcbal/Printable-AZERTY-NF>