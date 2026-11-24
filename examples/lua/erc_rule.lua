-- Proposed Amb3r host adapter, NOT a stock Mune module.
-- No io/os/require/network. Host supplies bounded snapshot and diagnostics.
local function check_power(snapshot)
    local pins = amb3r.objects(snapshot, "pin", 128)
    for i = 1, #pins do
        local p = pins[i]
        if p.required and p.kind == "power_in" and not p.connected then
            amb3r.emit("ERC.POWER_UNCONNECTED", p.id, "Required supply pin is unconnected")
        end
    end
end
amb3r.rule("example.power", check_power)
