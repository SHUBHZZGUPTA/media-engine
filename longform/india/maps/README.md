# India video: map borders

Shubham's call (29 Oct 2026): use India's official boundary as published by the Government of India / Survey of India, with all of Jammu & Kashmir and Ladakh inside India.

- `ne_50m_admin_0_countries_ind.geojson`: Natural Earth (public domain) admin-0 countries, India point-of-view edition (`ne_10m_admin_0_countries_ind`), simplified to ~50m detail. India's polygon includes PoK, Gilgit-Baltistan, Aksai Chin, Shaksgam and Arunachal Pradesh, matching the official political map.
- Use it by setting `MAP_COUNTRIES=longform/india/maps/ne_50m_admin_0_countries_ind.geojson` when running `engine/maps.py` or the 3D globe overlays (`engine/map3d/overlays.py`). Unset = default borders (other videos unchanged).
- `india_official_check.png`: proof render.
