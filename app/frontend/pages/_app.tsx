/* eslint-disable @next/next/inline-script-id */
import "../styles/globals.css";
import type { AppProps } from "next/app";
import { init as initApm } from "@elastic/apm-rum";

var apm = initApm({
  serviceName: "frontend-next-js",
  serverUrl: "http://localhost:8200",
  distributedTracingOrigins: ["http://localhost:9000"],
});

export default function App({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}
