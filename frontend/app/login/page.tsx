"use client";
import { SignIn } from "@clerk/nextjs";
export default function LoginPage(){return <div className="min-h-[80vh] grid place-items-center"><SignIn routing="hash" signUpUrl="/register" /></div>}
