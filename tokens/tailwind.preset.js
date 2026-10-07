/** ASQARA.TECH Tailwind preset — colours resolve to tokens.css variables. */
module.exports = {
  theme: {
    extend: {
      colors: {
        bg: "var(--bg)",
        surface: "var(--surface)",
        border: "var(--border)",
        text: "var(--text)",
        muted: "var(--muted)",
        violet: "var(--violet)",
        lime: { DEFAULT: "var(--lime)", ink: "var(--lime-ink)" },
        "on-lime": "var(--on-lime)",
      },
      fontFamily: { sans: ["var(--font-sans)"], mono: ["var(--font-mono)"] },
      borderRadius: { none: "0", DEFAULT: "0" },
      letterSpacing: { display: "-0.04em", label: "0.12em" },
      spacing: { grid: "40px", header: "var(--header-height)" },
      maxWidth: { shell: "1500px" },
      transitionTimingFunction: { "out-expo": "cubic-bezier(.16,1,.3,1)" },
      keyframes: {
        rise: { from: { opacity: "0", transform: "translateY(16px)" } },
        pulse: { to: { transform: "scale(3.2)", opacity: "0" } },
        flow: { to: { strokeDashoffset: "-20" } },
      },
      animation: {
        rise: "rise .9s cubic-bezier(.16,1,.3,1) both",
        ping: "pulse 2.2s ease-out infinite",
        flow: "flow .9s linear infinite",
        "spin-slow": "spin 14s linear infinite",
      },
    },
  },
};
