# GitHub profile review

Reviewed 10 October 2026. This is a review of the public profile and source repositories, with experience supplied by Vaibhav's résumé. It is not a runtime or security audit of the projects.

## Current profile

[ThomasShelby4477](https://github.com/ThomasShelby4477) has ten public repositories, no profile README, and no public name, bio, company, location, or contact details in its API response. The overview shows “Popular repositories,” led by Phone Detection and Turn on Light, rather than a deliberately curated set of recent work. The profile publicly displays 175 contributions over its rolling year.

The account handle gives little information about Vaibhav's professional identity. The first screen should establish his name, cybersecurity background, software work, and a clear route to selected projects and contact.

## Professional examples and design decisions

- [Anthony Fu](https://github.com/antfu): compact navigation and carefully chosen repository pins make deeper work easy to reach. Adopt short navigation and deliberate project selection.
- [Sindre Sorhus](https://github.com/sindresorhus): a precise sidebar bio and a concise route to current work. Adopt a focused professional identity and useful destinations.
- [Sebastián Ramírez](https://github.com/tiangolo): introduces himself through the tools he has built, then provides direct contact links. Adopt a clear connection between the person and their work.
- [Anurag Hazra](https://github.com/anuraghazra): connects professional experience with concrete project outcomes. Adopt résumé-backed experience and measured claims where the résumé provides them.

- [Aarsh Chaurasia](https://github.com/aarshx05), supplied by Vaibhav: current-focus context, grouped skills, direct branded contact links, and a dedicated statistics section. Adopt those organisational ideas with original typography, palette, artwork, and project cards. No biography, credentials, achievements, or wording copied.

These examples inform the hierarchy. Their copy, artwork, and achievements are not reused.

GitHub is a Markdown surface with sanitised HTML, rather than a freeform website. The draft uses native headings, links, a skills table, a collapsible archive, and SVG images. Custom artwork covers the header, branded links, project cards, toolkit, education, statistics overview, and activity dashboard. Project summaries, experience, skills, degree status, and contacts also remain native, searchable text. All major cards have phone/desktop SVGs. Artwork deliberately stays dark in either GitHub theme; the surrounding GitHub shell follows the visitor’s settings.

## Recommended order

1. Name, professional positioning, custom header, short navigation.
2. Brief introduction, branded LinkedIn/Gmail/GitHub/Maskr links, and a compact statistics overview.
3. Current focus: role, building interests, and M.Tech studies.
4. Selected work: Maskr, Codebase Architect, CampusNest, KreedaScore.
5. Experience: Delhivery, RailTel, and Parakram technical leadership.
6. Skills grouped by security, engineering, data, and AI.
7. Education and the CEH qualification explicitly marked in progress.
8. GitHub activity with clear data scope.
9. Contact links and a concise invitation to connect.

Projects appear early because visitors can inspect them directly. Employment and education add context. The compact numbers appear near the introduction; the detailed activity dashboard follows the work and background.

## Project evidence

| Project | Evidence inspected | Presentation decision |
| --- | --- | --- |
| Maskr | Résumé and [live Chrome Web Store listing](https://chromewebstore.google.com/detail/maskr-private-ai-leak-gua/adncldmdaamhlpcccigfhdipjhpicebe); official listing showed v1.1.1, updated 6 October 2026 | Feature first as a published privacy product. Link to the store and policy; the policy repository is not presented as extension source. |
| Codebase Architect | [README](https://github.com/ThomasShelby4477/CodeBase-Architect), pyproject, repository tree, MCP tool implementation | Feature AST parsing, graph storage, semantic retrieval, and MCP. Avoid unverified performance claims. |
| CampusNest | [Repository](https://github.com/ThomasShelby4477/campusnest), package manifest, source tree, résumé; configured website returned HTTP 200 | Feature a full-stack product with authentication, private documents, maps, and payments. HTTP availability does not establish end-to-end functionality. |
| KreedaScore | [Repository](https://github.com/ThomasShelby4477/sports-week-score-app), client/server manifests, Home component, routes; configured website returned HTTP 200; résumé leadership section | Feature real-time sports workflows and technical leadership. |
| Satellite Telemetry | [Repository](https://github.com/ThomasShelby4477/Satellite-Malware-Detection), README, source tree | Include in the project archive. Do not promote the README's 100% recall as a validated real-world result. |
| SecureVault | [Repository](https://github.com/ThomasShelby4477/securevault), crypto engine, file routes, requirements | Include as an encryption/file-management project. No security certification or audit claim. |
| Chess Analyser Pro | [Repository](https://github.com/ThomasShelby4477/Chess_Analyser_Pro), README, repository tree | Include as an experiment. The main analyser and pretrained model named by the README were absent from the inspected tree. |

Vaibhav subsequently clarified that B.Tech is completed and M.Tech has started. The draft now displays those statuses separately. No B.Tech completion date was inferred; the résumé’s expected August 2027 end date is retained for M.Tech.

Employment, dates, original education details, the 500K+ daily-event figure, and the 15% false-positive reduction come from the supplied résumé. They are user-supplied professional claims, not independently verified employer records. LinkedIn's public URL was taken from the résumé; the page redirected to a sign-in wall, so its contents were not independently reviewed.

## Repository presentation improvements

| Repository | Proposed description | Suggested topics |
| --- | --- | --- |
| CodeBase-Architect | MCP server for structure-aware codebase search, dependency graphs, and AI assistant context. | mcp, developer-tools, python, tree-sitter, semantic-search |
| campusnest | Student housing and roommate platform with verification, maps, messaging, and payments. | nextjs, typescript, supabase, student-housing, full-stack |
| sports-week-score-app | Live sports-event scores, tournament brackets, medal tallies, and organiser workflows. | react, express, postgresql, sports, real-time |
| securevault | Flask file-management app with encryption, authenticated access, and audit logging. | flask, python, encryption, file-management |

The four repositories above currently lack descriptions. KreedaScore and SecureVault also lack root READMEs. Before presenting them as finished case studies, add a screenshot, purpose, architectural summary, local setup, configuration reference, and explicit project limitations.

Codebase Architect's quickstart currently uses `your-org/codebase-architect`; replace that placeholder with the actual repository URL. Chess Analyser Pro's setup references files not present in its public tree; repair those instructions before promoting it as runnable.

## Sidebar and pins

Recommended sidebar name: **Vaibhav Yadav**.

Recommended bio: **Cybersecurity, risk analytics & software engineering. Building on-device privacy tools, AI developer infrastructure and full-stack products.**

Add the résumé's LinkedIn link as a social link. Add email as a README contact link. Maskr's store listing remains in selected work; a dedicated portfolio URL can be added later if one exists.

Recommended pin order: Codebase Architect, CampusNest, KreedaScore, Satellite Telemetry, Auditorium Booking Portal, then SecureVault after adding its README. Maskr has no inspected public source repository, so its store link carries that project. GitHub permits [up to six pinned items](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/pinning-items-to-your-profile).

## Activity implementation

The upstream [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats) README now states that the project is no longer maintained, and describes the shared public service as best effort. This draft instead stores its own SVG cards in the profile repository.

The scheduled workflow retrieves public repository metrics and the full publicly displayed contribution calendar. Calendar cells are matched to GitHub tooltips for exact daily counts. The collected calendar must contain consecutive dates and reconcile with the headline total before any assets are replaced. It derives active days, calendar-day streaks, a peak day, and monthly totals, including partial boundary months. The chart does not imply continuous daily activity. It uses GitHub's built-in workflow token for API capacity; no external stats service or personal token is required. Repository enumeration explicitly excludes private repos and forks. The contribution count uses the public profile's rolling year, including any activity GitHub already elects to display publicly.

Fetch failures fail the workflow and retain the previous committed cards. Snapshot dates stay visible. The daily refresh has been prepared and the script has run locally; the hosted schedule has not run because the profile repository is not yet published.

## Platform references

- [Managing your profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme): the public repository must match the username and have a root README.
- [Pinning items](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/pinning-items-to-your-profile): pin selection and ordering.
- [GitHub Markdown CSS](https://github.com/sindresorhus/github-markdown-css): local preview styling. The Markdown itself is rendered by GitHub's API.

## Validation boundary

Completed checks: GitHub Markdown API rendering; all generated SVG assets parsed as XML with accessibility titles; live public statistics collection and offline rebuilding; Python script compilation; workflow YAML parsing; visual inspection at 1280px desktop and 390px phone widths in light and dark themes. The browser confirmed all responsive image assets loaded at each tested breakpoint and there was no page-wide horizontal overflow. The activity navigation reached its heading. The complete desktop page was also visually inspected.

The preview is a local approximation using GitHub-rendered Markdown and GitHub-style CSS. Publication is required to verify the actual profile shell, sidebar, repository pins, remote asset URLs, and hosted GitHub Actions. Nothing has been published or changed on the account.

## Visual refresh validation · 10 October 2026

The brutalist dark refresh uses near-black (#10120f), off-white (#f2f3e8), acid green (#c6ff00), and burnt orange (#ff773d), with square panels, heavy borders, and bold monospace artwork. The refresh includes branded contact badges, original project cards, a skills table, separate degree-status panels, a public contribution heatmap and a full-width monthly chart. Live collection reconciled 175 contributions across 19 active days, a longest streak of 3 days, and a peak of 42 contributions. Ten public owned repositories earned one star. Language distribution was removed at Vaibhav’s request. The calendar parser was checked against year-boundary, zero-activity, and incomplete-data cases. SVG XML parsing, GitHub Markdown rendering, and phone/desktop visual checks pass. Remote publication and the hosted workflow remain unverified.

## Header animation · 10 October 2026

The header now types the name once, then cycles three taglines: Security × Software, Privacy by Design, and AI Developer Tools. Each tagline gets an eight-second slot with character-by-character typing, a long reading pause, and faster deletion. Geometry remains fixed throughout the animation. The cursor fades gently. The artwork is self-contained, with CSS for the name/cursor and native SVG timing for the tagline; it requires no JavaScript, external fonts, or animation service.

A prefers-reduced-motion rule reveals the complete name and a static tagline. A local inspection fixture activates those same rules for visual checking without changing the user's system preferences. The generated animation timelines and SVG XML were validated; desktop/phone preview rendering and the static fallback were inspected. Actual GitHub asset delivery remains pending publication.

References: [Readme Typing SVG](https://github.com/DenverCoder1/readme-typing-svg) demonstrates animated SVGs in profile READMEs; [MDN SVG animation](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_animation_with_SMIL) documents the native timing mechanism, and [MDN reduced motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion) documents the media query. The animation here is original code, without source copied from the example.
