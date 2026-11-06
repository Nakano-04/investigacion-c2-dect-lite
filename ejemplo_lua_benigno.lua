-- scope: lab-only
c2.log("INFO", "hola desde " .. c2.session_id())

local info = c2.task("sysinfo")
if info then
    c2.log("INFO", info)
end

return "listo"
