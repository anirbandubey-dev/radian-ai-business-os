export function GlassCard({children,className=""}:{children:React.ReactNode;className?:string}){return <div className={`glass rounded-xl p-5 ${className}`}>{children}</div>}
export function StatCard({label,value,detail}:{label:string;value:string;detail:string}){return <GlassCard><div className="text-sm text-muted">{label}</div><div className="text-3xl font-semibold mt-3">{value}</div><div className="text-xs text-accent mt-2">{detail}</div></GlassCard>}

