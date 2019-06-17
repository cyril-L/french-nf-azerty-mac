# Pilotes macOS pour le nouveau clavier AZERTY normalisé

Utilisez votre clavier existant pour tester la nouvelle disposition des symboles. Vous pouvez l’apprendre en vous aidant du clavier virtuel de macOS ou du site <https://norme-azerty.fr>.

Ce pilote implémente :

- l’ensemble des caractères requis pour saisir du texte en français (par exemple É, œ et «)
- le « Mode monétaire »
- le « Mode lettres grecques »
- le « Mode caractères européens »

Il n’implémente pas encore la plupart des diacritiques peu utilisés en France.

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

Pour mettre à jour le pilote, remplacez le fichier `.bundle` existant et redémarrez votre session.

## Contribution

- Rapportez un problème ou une suggestion sur la page [Issues](https://github.com/cyril-L/normalized-azerty/issues)
- Modifiez la disposition et soumettez une *Pull Request*
- La disposition a été créée avec le logiciel [Ukelele](http://scripts.sil.org/ukelele). Il est aussi possible de modifier directement le fichier [French - NF.keylayout](https://github.com/cyril-L/normalized-azerty/blob/master/French%20NF.bundle/Contents/Resources/French%20-%20NF.keylayout) manuellement.
- La disposition suit la description présentée sur le site <https://norme-azerty.fr>.
- Les caractères Unicode ont principalement été récupérés sur :
  - <https://bepo.fr/wiki/Touches_mortes>
  - <https://github.com/marcbal/Printable-AZERTY-NF>