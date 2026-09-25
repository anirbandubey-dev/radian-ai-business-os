import type { Config } from "tailwindcss";
export default { content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"], theme: { extend: { colors: { ink: "#080b12", panel: "#111722", line: "#273143", muted: "#8d99ad", accent: "#7c8cff" } } }, plugins: [] } satisfies Config;
