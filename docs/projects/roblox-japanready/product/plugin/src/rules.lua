--!strict

export type RuleInput = {
	text: string,
	textLength: number,
	autoLocalize: boolean?,
	localizationMatchIdentifier: string?,
}

export type RuleOptions = {
	longTextThreshold: number?,
}

local Rules = {}

local DEFAULT_LONG_TEXT_THRESHOLD = 80

local function appendWarning(warnings: { string }, code: string)
	table.insert(warnings, code)
end

function Rules.evaluate(input: RuleInput, options: RuleOptions?): { string }
	local threshold = DEFAULT_LONG_TEXT_THRESHOLD
	if options and options.longTextThreshold then
		threshold = math.max(1, math.floor(options.longTextThreshold))
	end

	local warnings: { string } = {}

	if input.autoLocalize == false then
		appendWarning(warnings, "AUTOLOCALIZE_DISABLED")
	end

	if input.textLength > threshold then
		appendWarning(warnings, "LONG_TEXT_REVIEW")
	end

	if string.find(input.text, "\n", 1, true) or string.find(input.text, "\r", 1, true) then
		appendWarning(warnings, "LINE_BREAK_REVIEW")
	end

	if input.autoLocalize == false
		and (input.localizationMatchIdentifier == nil or input.localizationMatchIdentifier == "")
	then
		appendWarning(warnings, "HARD_CODED_TEXT_CANDIDATE")
	end

	return warnings
end

function Rules.defaultLongTextThreshold(): number
	return DEFAULT_LONG_TEXT_THRESHOLD
end

return Rules
