"use client";
import React from "react";
import { useState, useEffect } from "react";
import Box1 from "./box1";
import { generateOutput } from "./generateoutput";

export default function Main() {
  const [loading, setLoading] = useState(false);
  const [postData, setpostData] = useState("");

  useEffect(() => {
    if (loading) {
      generateOutput(
        setLoading,
        setpostData
      );
    }
  }, [loading]);

  return (
    <div className="flex-grow grid mx-4 my-6 space-x-4">
      <div className="glass">
        <Box1
          loading={loading}
          setLoading={setLoading}
          postData={postData}
        />
      </div>
    </div>
  );
}
