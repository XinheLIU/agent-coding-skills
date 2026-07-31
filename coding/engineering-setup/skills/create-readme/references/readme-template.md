# README Template

Last updated: 2026-07-18

Structural blueprint adapted from [othneildrew/Best-README-Template](https://github.com/othneildrew/Best-README-Template) (MIT).
Trim to the tier chosen in Phase 2. Replace ALL placeholders (`{{...}}`) — never ship them.

Tier guide:

- **Minimal** — keep: About, Getting Started, Usage
- **Standard** — add: Built With, Project Structure, Roadmap, Contact
- **Full** — add: badges, logo header, ToC, Contributing, Acknowledgments, back-to-top links

---

```markdown
<a id="readme-top"></a>

<!-- FULL TIER: badges — only include badges that are TRUE for this repo -->
[![Contributors][contributors-shield]][contributors-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

<!-- FULL TIER: logo header — only if a logo/icon exists in the repo -->
<div align="center">
  <a href="{{repo_url}}">
    <img src="{{logo_path}}" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">{{project_title}}</h3>

  <p align="center">
    {{one_line_description}}
    <br />
    <a href="{{docs_url}}"><strong>Explore the docs »</strong></a>
    <br />
    <a href="{{demo_url}}">View Demo</a>
    &middot;
    <a href="{{repo_url}}/issues/new?labels=bug">Report Bug</a>
    &middot;
    <a href="{{repo_url}}/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>

<!-- FULL TIER: table of contents — anchors MUST match the headings you keep -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

<!-- Screenshot or demo GIF here if one exists -->

{{2-4 sentences: the problem this solves (WHY), what it does (WHAT), who it's for.
Lead with why. No feature laundry list — that's what Usage is for.}}

### Built With

<!-- STANDARD+: major frameworks/tools only, from the actual manifest -->
* {{framework_1}}
* {{framework_2}}

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

{{Runtime + version, package manager, external services. Everything a fresh
machine needs — verified, not assumed.}}

### Installation

<!-- Every command copy-pasteable and verified against the repo's manifest/scripts -->
1. Clone the repo
   ```sh
   git clone {{repo_url}}.git
   ```
2. Install dependencies
   ```sh
   {{install_command}}
   ```
3. Configure environment
   ```sh
   {{config_step — explain each env var a newcomer couldn't guess}}
   ```
4. Run
   ```sh
   {{run_command}}
   ```

> [!NOTE]
> {{First-run gotchas, if any: seed data, API keys, ports.}}

## Usage

{{Real, runnable examples with real output. Screenshots where they help.
Explain non-obvious flags, units, and abbreviations. Link to full docs if they exist.}}

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Project Structure

<!-- STANDARD+: only for non-trivial layouts; annotate WHAT each area owns -->
```text
{{project}}/
├── {{dir_1}}/    # {{what it owns}}
├── {{dir_2}}/    # {{what it owns}}
└── {{file}}      # {{why it matters}}
```

## Roadmap

- [ ] {{planned_feature_1}}
- [ ] {{planned_feature_2}}

See the [open issues]({{repo_url}}/issues) for the full list.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

<!-- FULL TIER: one-line pointer only — do NOT inline CONTRIBUTING.md content -->
Contributions are welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md).

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

<!-- One-line pointer only — do NOT inline license text -->
Distributed under the {{license_name}} license. See [`LICENSE`](LICENSE) for details.

## Contact

{{name}} — {{contact_handle_or_email}}

Project link: [{{repo_url}}]({{repo_url}})

## Acknowledgments

<!-- FULL TIER: real credits only; drop the section if empty -->
* {{credit_1}}

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES (reference-style, keeps the body readable) -->
[contributors-shield]: https://img.shields.io/github/contributors/{{owner}}/{{repo}}.svg?style=for-the-badge
[contributors-url]: {{repo_url}}/graphs/contributors
[stars-shield]: https://img.shields.io/github/stars/{{owner}}/{{repo}}.svg?style=for-the-badge
[stars-url]: {{repo_url}}/stargazers
[issues-shield]: https://img.shields.io/github/issues/{{owner}}/{{repo}}.svg?style=for-the-badge
[issues-url]: {{repo_url}}/issues
[license-shield]: https://img.shields.io/github/license/{{owner}}/{{repo}}.svg?style=for-the-badge
[license-url]: {{repo_url}}/blob/main/LICENSE
```
