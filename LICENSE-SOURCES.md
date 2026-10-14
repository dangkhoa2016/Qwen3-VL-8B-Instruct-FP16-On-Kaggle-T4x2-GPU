# Asset Sources and Licensing

All image assets distributed with this repository are project-generated benchmark assets. No third-party web photograph is required by the release showcase.

## AI-generated photorealistic assets

The six JPEG files under `examples/realistic/` were generated specifically for this project using OpenAI image generation, then resized to 1024×768 for reproducible Kaggle inference. They are synthetic benchmark images; they are not photographs downloaded from the web.

The depicted organizations, names, addresses, identifiers, prices and event details are fictional benchmark content. No real trademark/logo is intentionally used.

## Programmatically generated assets

The remaining benchmark PNG assets under `examples/` were generated specifically for this repository using drawing/chart code and fictional data.

## Release policy

- Do not add arbitrary Internet images to the release asset set.
- If a future third-party asset is introduced, record its source URL, author, license, modifications and redistribution basis before commit.
- Keep asset hashes in `ASSET_MANIFEST.json` so reviewer-visible inputs are reproducible.
