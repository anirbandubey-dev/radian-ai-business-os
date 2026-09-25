import { SignUp } from "@clerk/nextjs";
export default function RegisterPage(){return <div className="min-h-[80vh] grid place-items-center"><SignUp routing="hash" signInUrl="/login" /></div>}
