import "./globals.css";
import { Shell } from "../components/shell";
import { ClerkProvider } from "@clerk/nextjs";
export default function RootLayout({ children }: Readonly<{children: React.ReactNode}>) { return <ClerkProvider><html lang="en"><body><Shell>{children}</Shell></body></html></ClerkProvider>; }

