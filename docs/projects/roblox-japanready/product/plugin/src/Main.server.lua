--!strict

-- Prototype only. The implementation agent must confirm current Roblox Studio
-- plugin APIs and run a manual Studio smoke test before publishing.

local Scanner = require(script.Parent.scanner)
local Csv = require(script.Parent.csv)
local Ui = require(script.Parent.ui)

local view = Ui.create(plugin)

local function setScanningState(isScanning: boolean)
	view.scanButton.Active = not isScanning
	view.scanButton.Text = if isScanning then "Scanning..." else "Scan current place"
end

local function runScan()
	setScanningState(true)
	view.statusLabel.Text = "Scanning DataModel"

	local ok, result = pcall(function()
		local findings = Scanner.scan(game, { longTextThreshold = 80 })
		return {
			findings = findings,
			csv = Csv.encode(findings),
		}
	end)

	if ok then
		view.output.Text = result.csv
		view.statusLabel.Text = string.format("%d text instances found", #result.findings)
	else
		view.output.Text = "Scan failed. No objects were changed.\n\n" .. tostring(result)
		view.statusLabel.Text = "Scan failed"
	end

	setScanningState(false)
end

view.scanButton.Activated:Connect(runScan)

view.toggleButton.Click:Connect(function()
	view.widget.Enabled = not view.widget.Enabled
end)

plugin.Unloading:Connect(function()
	-- No persistent connection, external request, telemetry, or asset mutation
	-- is created by this prototype.
end)
