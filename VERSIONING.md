# Versioning & Releases

This project follows Semantic Versioning (`MAJOR.MINOR.PATCH`).

## Release Types

### Patch Releases

Patch releases are for bug fixes, small fixes, and other routine changes.

Version format:

```text
x.x.PATCH
```

Example:

```text
0.1.1
0.1.2
0.1.3
```

Use the commit message:

```bash
git commit -m "Bump version to x.x.x"
```

Create a **lightweight tag**:

```bash
git tag x.x.x
git push origin x.x.x
```

Example:

```bash
git commit -m "Bump version to 0.1.1"
git tag 0.1.1
git push origin 0.1.1
```

---

### Minor Releases

Minor releases are for new features and other backwards-compatible changes.

Version format:

```text
x.MINOR.0
```

Example:

```text
0.2.0
0.3.0
0.4.0
```

Use the commit message:

```bash
git commit -m "Release version x.x.x"
```

Create an **annotated tag**:

```bash
git tag -a x.x.x -m "Release version x.x.x"
git push origin x.x.x
```

Example:

```bash
git commit -m "Release version 0.2.0"
git tag -a 0.2.0 -m "Release version 0.2.0"
git push origin 0.2.0
```

---

### Major Releases

Major releases are for breaking changes or other significant milestones.

Version format:

```text
MAJOR.0.0
```

Example:

```text
1.0.0
2.0.0
```

Use the same convention as minor releases:

```bash
git commit -m "Release version x.x.x"
git tag -a x.x.x -m "Release version x.x.x"
git push origin x.x.x
```

Example:

```bash
git commit -m "Release version 1.0.0"
git tag -a 1.0.0 -m "Release version 1.0.0"
git push origin 1.0.0
```

---

## Quick Reference

| Release | Example | Commit message          | Tag type    |
| ------- | ------- | ----------------------- | ----------- |
| Patch   | `0.1.1` | `Bump version to 0.1.1` | Lightweight |
| Minor   | `0.2.0` | `Release version 0.2.0` | Annotated   |
| Major   | `1.0.0` | `Release version 1.0.0` | Annotated   |

### Tag Convention

* **`Bump version to x.x.x` → lightweight tag**
* **`Release version x.x.x` → annotated tag**

This distinction is intentional: lightweight tags are used for routine patch releases, while annotated tags identify significant minor and major releases.

## Automated Releases

Pushing a version tag matching the project's release workflow triggers the automated release process.

The release workflow builds the package and publishes the distributions to PyPI and GitHub Releases.

For example:

```bash
git push origin 0.1.1
```

or:

```bash
git push origin 0.2.0
```

will trigger the release workflow.
