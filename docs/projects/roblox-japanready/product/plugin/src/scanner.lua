--!strict

export type Finding = {
	path: string,
	className: string,
	name: string,
	text: string,
	textLength: number,
	autoLocalize: boolean?,
	localizationMatchIdentifier: string?,
	warnings: { string },
}

local Scanner = {}

local TEXT_CLASSES = {
	TextLabel = true,
	TextButton = true,
	TextBox = true,
}

local DEFAULT_LONG_TEXT_THRESHOLD = 80

local function safeRead(instance: Instance, propertyName: string): any
	local ok, value = pcall(function()
		return (instance :: any)[propertyName]
	end)
	if ok then
		return value
	end
	return nil
end

local function instancePath(instance: Instance): string
	local parts: { string } = {}
	local cursor: Instance? = instance
	while cursor ~= nil and cursor ~= game do
		table.insert(parts, 1, cursor.Name)
		cursor = cursor.Parent
	end
	return "game." .. table.concat(parts, ".")
end

local function appendWarning(warnings: { string }, code: string)
	table.insert(warnings, code)
end

local function scanTextInstance(instance: Instance, longTextThreshold: number): Finding?
	if not TEXT_CLASSES[instance.ClassName] then
		return nil
	end

	local rawText = safeRead(instance, "Text")
	if typeof(rawText) ~= "string" or rawText == "" then
		return nil
	end

	local autoLocalize = safeRead(instance, "AutoLocalize")
	local matchIdentifier = safeRead(instance, "LocalizationMatchIdentifier")
	local warnings: { string } = {}

	if autoLocalize == false then
		appendWarning(warnings, "AUTOLOCALIZE_DISABLED")
	end
	if #rawText > longTextThreshold then
		appendWarning(warnings, "LONG_TEXT_REVIEW")
	end
	if string.find(rawText, "\n", 1, true) or string.find(rawText, "\r", 1, true) then
		appendWarning(warnings, "LINE_BREAK_REVIEW")
	end
	if autoLocalize == false and (matchIdentifier == nil or matchIdentifier == "") then
		appendWarning(warnings, "HARD_CODED_TEXT_CANDIDATE")
	end

	return {
		path = instancePath(instance),
		className = instance.ClassName,
		name = instance.Name,
		text = rawText,
		textLength = utf8.len(rawText) or #rawText,
		autoLocalize = if typeof(autoLocalize) == "boolean" then autoLocalize else nil,
		localizationMatchIdentifier = if typeof(matchIdentifier) == "string" then matchIdentifier else nil,
		warnings = warnings,
	}
end

function Scanner.scan(root: Instance, options: { longTextThreshold: number? }?): { Finding }
	local threshold = DEFAULT_LONG_TEXT_THRESHOLD
	if options and options.longTextThreshold then
		threshold = math.max(1, math.floor(options.longTextThreshold))
	end

	local findings: { Finding } = {}
	for _, descendant in root:GetDescendants() do
		local finding = scanTextInstance(descendant, threshold)
		if finding then
			table.insert(findings, finding)
		end
	end

	table.sort(findings, function(a, b)
		if a.path == b.path then
			return a.text < b.text
		end
		return a.path < b.path
	end)

	return findings
end

return Scanner
