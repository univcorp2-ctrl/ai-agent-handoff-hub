--!strict

local Rules = require(script.Parent.rules)

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

export type ScanOptions = {
	longTextThreshold: number?,
}

local Scanner = {}

local TEXT_CLASSES: { [string]: boolean } = {
	TextLabel = true,
	TextButton = true,
	TextBox = true,
}

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

local function scanTextInstance(instance: Instance, options: ScanOptions?): Finding?
	if not TEXT_CLASSES[instance.ClassName] then
		return nil
	end

	local rawText = safeRead(instance, "Text")
	if typeof(rawText) ~= "string" or rawText == "" then
		return nil
	end

	local characterCount = utf8.len(rawText) or #rawText
	local autoLocalize = safeRead(instance, "AutoLocalize")
	local matchIdentifier = safeRead(instance, "LocalizationMatchIdentifier")
	local normalizedAutoLocalize = if typeof(autoLocalize) == "boolean" then autoLocalize else nil
	local normalizedMatchIdentifier = if typeof(matchIdentifier) == "string" then matchIdentifier else nil

	local warnings = Rules.evaluate({
		text = rawText,
		textLength = characterCount,
		autoLocalize = normalizedAutoLocalize,
		localizationMatchIdentifier = normalizedMatchIdentifier,
	}, options)

	return {
		path = instancePath(instance),
		className = instance.ClassName,
		name = instance.Name,
		text = rawText,
		textLength = characterCount,
		autoLocalize = normalizedAutoLocalize,
		localizationMatchIdentifier = normalizedMatchIdentifier,
		warnings = warnings,
	}
end

function Scanner.scan(root: Instance, options: ScanOptions?): { Finding }
	local findings: { Finding } = {}
	for _, descendant in ipairs(root:GetDescendants()) do
		local finding = scanTextInstance(descendant, options)
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
