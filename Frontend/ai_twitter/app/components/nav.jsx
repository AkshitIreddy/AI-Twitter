import React from "react";

export default function Nav() {
  return (
    <div className="mt-4 mx-4">
      <nav className={`glass flex items-center justify-between px-8 py-2`}>
        <div className="flex items-center">
          <h1 className="gradtext mb-0 pb-0 text-2xl font-bold text-gray-700">
            AI Twitter
          </h1>
        </div>
        <div className="flex items-center text-xl font-bold text-gray-600">
          <a href="#" className="mr-4 pl-2 hover:text-white ">
            Large Language Models
          </a>
          <a
            href="#"
            className="mr-4 border-l-2 pl-2 hover:text-white border-zinc-500"
          >
            Stable Diffusion
          </a>
          <a
            href="#"
            className="mr-4 border-l-2 pl-2 hover:text-white border-zinc-500"
          >
            Nextjs
          </a>
        </div>
      </nav>
    </div>
  );
}
