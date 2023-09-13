import { defineConfig, loadEnv } from "vite";
import vue from "@vitejs/plugin-vue";

const path = require("path");

// https://vitejs.dev/config/
// eslint-disable-next-line no-unused-vars
export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  return {
    plugins: [vue()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    base: env.VITE_PUBLIC_PATH,
    test: {
      environment: "happy-dom",
      coverage: {
        reporter: ["text", "json", "lcov"],
      },
    },
  };
});
