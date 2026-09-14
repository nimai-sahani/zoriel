# Zoriel Architecture Notes

## v0.3.0 foundation

The existing v0.2.1 consumer application remains the canonical starting point. v0.3 separates domain responsibilities without pretending that production commerce integrations exist.

### Boundaries

- `packages/schemas`: contracts shared between services and clients.
- `services/ai`: intent understanding and future Orion tool-calling logic.
- `services/search`: catalogue discovery and ranking.
- `services/commerce`: provider-agnostic commerce boundary.
- `adapters/`: future ONDC, merchant, logistics and payment implementations.

### Non-negotiable

No simulated payment, fake live availability, fake ONDC confirmation, or fake successful order may be presented as real.
