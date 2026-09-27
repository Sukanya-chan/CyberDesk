import React from "react";
import ReactDOM from "react-dom/client";

import { App } from "./app/App";
import { ClerkProviderWrapper } from "./app/ClerkProviderWrapper";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <ClerkProviderWrapper>
      <App />
    </ClerkProviderWrapper>
  </React.StrictMode>,
);
