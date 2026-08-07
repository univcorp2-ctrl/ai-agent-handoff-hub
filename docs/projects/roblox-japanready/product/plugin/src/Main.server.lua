--!strict

-- Prototype only. The implementation agent must confirm current Roblox Studio
-- plugin APIs and run a manual Studio smoke test before publishing.

local Scanner = require(script.Parent.scanner)
local Csv = require(script.Parent.csv)

local TOOLBAR_NAME = "JapanReady"
local BUTTON_ID = "JapanReadyScan"
local WIDGET_ID = "JapanReadyLocalizationAudit"

local toolbar = plugin:CreateToolbar(TOOLBAR_NAME)
local toggleButton = toolbar:CreateButton(
	BUTTON_ID,
	"Scan player-facing text for Japanese localization risks",
	""
)
toggleButton.ClickableWhenViewportHidden = true

local widgetInfo = DockWidgetPluginGuiInfo.new(
	Enum.InitialDockState.Float,
	false,
	false,
	760,
	560,
	360,
	260
)

local widget = plugin:CreateDockWidgetPluginGui(WIDGET_ID, widgetInfo)
widget.Title = "JapanReady Localization Audit"

local rootFrame = Instance.new("Frame")
rootFrame.Name = "Root"
rootFrame.Size = UDim2.fromScale(1, 1)
rootFrame.BackgroundColor3 = Color3.fromRGB(245, 246, 248)
rootFrame.Parent = widget

local padding = Instance.new("UIPadding")
padding.PaddingTop = UDim.new(0, 12)
padding.PaddingRight = UDim.new(0, 12)
padding.PaddingBottom = UDim.new(0, 12)
padding.PaddingLeft = UDim.new(0, 12)
padding.Parent = rootFrame

local title = Instance.new("TextLabel")
title.Name = "Title"
title.BackgroundTransparency = 1
title.Size = UDim2.new(1, 0, 0, 32)
title.Font = Enum.Font.SourceSansBold
title.TextSize = 22
title.TextXAlignment = Enum.TextXAlignment.Left
title.Text = "JapanReady — read-only text audit"
title.Parent = rootFrame

local explanation = Instance.new("TextLabel")
explanation.Name = "Explanation"
explanation.BackgroundTransparency = 1
explanation.Position = UDim2.new(0, 0, 0, 34)
explanation.Size = UDim2.new(1, 0, 0, 44)
explanation.Font = Enum.Font.SourceSans
explanation.TextSize = 15
explanation.TextWrapped = true
explanation.TextXAlignment = Enum.TextXAlignment.Left
explanation.TextYAlignment = Enum.TextYAlignment.Top
explanation.Text = "Scans TextLabel, TextButton, and TextBox instances. It does not modify objects or send data outside Studio."
explanation.Parent = rootFrame

local scanButton = Instance.new("TextButton")
scanButton.Name = "Scan"
scanButton.Position = UDim2.new(0, 0, 0, 86)
scanButton.Size = UDim2.new(0, 180, 0, 36)
scanButton.Font = Enum.Font.SourceSansBold
scanButton.TextSize = 17
scanButton.Text = "Scan current place"
scanButton.Parent = rootFrame

local statusLabel = Instance.new("TextLabel")
statusLabel.Name = "Status"
statusLabel.BackgroundTransparency = 1
statusLabel.Position = UDim2.new(0, 192, 0, 86)
statusLabel.Size = UDim2.new(1, -192, 0, 36)
statusLabel.Font = Enum.Font.SourceSans
statusLabel.TextSize = 15
statusLabel.TextXAlignment = Enum.TextXAlignment.Left
statusLabel.Text = "Not scanned"
statusLabel.Parent = rootFrame

local output = Instance.new("TextBox")
output.Name = "CsvOutput"
output.Position = UDim2.new(0, 0, 0, 132)
output.Size = UDim2.new(1, 0, 1, -132)
output.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
output.ClearTextOnFocus = false
output.Font = Enum.Font.Code
output.MultiLine = true
output.TextEditable = true
output.TextSize = 13
output.TextWrapped = false
output.TextXAlignment = Enum.TextXAlignment.Left
output.TextYAlignment = Enum.TextYAlignment.Top
output.Text = "Run a scan. Then select and copy the CSV text manually."
output.Parent = rootFrame

local function runScan()
	scanButton.Active = false
	scanButton.Text = "Scanning..."
	statusLabel.Text = "Scanning DataModel"

	local ok, result = pcall(function()
		local findings = Scanner.scan(game, { longTextThreshold = 80 })
		return {
			findings = findings,
			csv = Csv.encode(findings),
		}
	end)

	if ok then
		output.Text = result.csv
		statusLabel.Text = string.format("%d text instances found", #result.findings)
	else
		output.Text = "Scan failed. No objects were changed.\n\n" .. tostring(result)
		statusLabel.Text = "Scan failed"
	end

	scanButton.Text = "Scan current place"
	scanButton.Active = true
end

scanButton.Activated:Connect(runScan)

toggleButton.Click:Connect(function()
	widget.Enabled = not widget.Enabled
end)

plugin.Unloading:Connect(function()
	-- No persistent connection, external request, or asset mutation to clean up.
end)
