import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#17211f",
        rail: "#245f73",
        mint: "#c8e4d8",
        amberline: "#e0a73f",
        danger: "#c94c4c"
      }
    }
  },
  plugins: []
};

export default config;
