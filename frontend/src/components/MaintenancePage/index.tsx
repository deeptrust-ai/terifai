import React from "react";
import { TwitterIcon } from "lucide-react";

import DeepTrustLogo from "../../assets/logos/deeptrust.png";

const MaintenancePage: React.FC = () => {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="max-w-md p-8 bg-white shadow-md rounded-lg text-center">
        <img
          src={DeepTrustLogo}
          alt="DeepTrust Logo"
          className="mx-auto mb-6 h-12"
        />
        <h1 className="text-3xl font-bold mb-4">We'll be back soon!</h1>
        <p className="text-gray-600 mb-4">
          Sorry for the inconvenience, but we're performing some maintenance at
          the moment. We'll be back online!
        </p>
        <p className="text-sm text-gray-500">
          —{" "}
          <a
            href="https://twitter.com/amanmibra"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center"
          >
            Aman Ibrahim <TwitterIcon className="ml-1 w-4 h-4" />
          </a>
        </p>
        <p className="text-xs text-gray-400 mt-2">
          From the{" "}
          <a
            href="https://twitter.com/deeptrustAI"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center"
          >
            DeepTrust Team <TwitterIcon className="ml-1 w-4 h-4" />
          </a>
        </p>
      </div>
    </div>
  );
};

export default MaintenancePage;
