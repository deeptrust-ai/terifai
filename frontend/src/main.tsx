import React from "react";
import ReactDOM from "react-dom/client";
import { DailyProvider } from "@daily-co/daily-react";
import { Analytics } from "@vercel/analytics/react";

import Header from "./components/ui/header.tsx";
import { TooltipProvider } from "./components/ui/tooltip.tsx";
import App from "./App.tsx";

import "./global.css"; // Note: Core app layout can be found here

// Show warning on Firefox
// @ts-expect-error - Firefox is not supported
const isFirefox: boolean = typeof InstallTrigger !== "undefined";

export const Layout = () => {
  return (
    <DailyProvider>
      <TooltipProvider>
        <main>
          <Header />
          <div id="app">
            <App />
          </div>
        </main>
        <aside id="tray" />
      </TooltipProvider>
    </DailyProvider>
  );
};

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    {isFirefox && (
      <div className="bg-red-500 text-white text-sm font-bold text-center p-2 fixed t-0 w-full">
        Voice activity detection not supported in Firefox. For best results,
        please use Chrome or Edge.
      </div>
    )}
    <Layout />
    <Analytics />
  </React.StrictMode>
);
