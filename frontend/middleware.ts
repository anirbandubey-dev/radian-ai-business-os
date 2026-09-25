import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";
const isProtectedRoute = createRouteMatcher(["/dashboard(.*)", "/accounts(.*)", "/contacts(.*)", "/leads(.*)", "/deals(.*)", "/activities(.*)", "/tasks(.*)", "/calendar(.*)", "/insights(.*)", "/predictions(.*)", "/recommendations(.*)", "/data(.*)", "/pipelines(.*)", "/inventory(.*)", "/production(.*)", "/suppliers(.*)", "/settings(.*)"]);
export default clerkMiddleware(async (auth, req) => { if (isProtectedRoute(req)) await auth.protect(); });
export const config = { matcher: ["/((?!_next|.*\\..*).*)", "/(api|trpc)(.*)"] };
