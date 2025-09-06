# Pull Request

## Summary
<!-- Briefly describe the changes in this PR -->

## Type of Change
<!-- Mark the appropriate option -->
- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🧪 Test improvements
- [ ] 🔧 Maintenance/refactoring
- [ ] 🚨 Security fix

## Framework Component
<!-- Check all components affected by this PR -->
- [ ] Prompt System (assets, registry, builder, strategies)
- [ ] Core Operations (C, D, F, X, Z, E matrices)
- [ ] LLM Integration (OpenAI Responses API)
- [ ] Combined Lensing
- [ ] CLI
- [ ] Exporters (Neo4j, JSONL, working memory)
- [ ] Tests
- [ ] Documentation
- [ ] CI/CD

## Changes Made
<!-- Provide a detailed description of what was changed -->

### Technical Changes
- 
- 
- 

### API Changes (if any)
- 
- 

## Testing
<!-- Describe how you tested these changes -->

### Tests Added/Modified
- [ ] Unit tests
- [ ] Integration tests  
- [ ] CLI tests
- [ ] Architecture tests

### Manual Testing Performed
<!-- Describe manual testing steps -->
- [ ] CLI smoke tests (`python -m chirality.cli info`)
- [ ] Echo resolver testing (`--resolver echo`)
- [ ] OpenAI resolver testing (`--resolver openai`) - if applicable
- [ ] Specific matrix operations: C / D / F / X / Z / E
- [ ] Other: _______________

## Semantic Integrity Compliance
<!-- CRITICAL: Confirm compliance with framework principles -->

### Maintainer Semantic Authority
- [ ] ✅ No AI-generated semantic content added to prompt assets
- [ ] ✅ Only maintainer-authored semantic modifications (if any)
- [ ] ✅ Prompt assets maintain SHA256 integrity
- [ ] ✅ No modification of `chirality/normative_spec.txt` without maintainer approval

### OpenAI API Compliance  
- [ ] ✅ Uses OpenAI Responses API exclusively (`responses.create`)
- [ ] ✅ No Chat Completions API usage (`chat.completions.create`)
- [ ] ✅ Maintains JSON response format requirements

### Architecture Compliance
- [ ] ✅ Maintains component-station separation (components map to stations, not vice versa)
- [ ] ✅ Uses combined lensing (not three-stage lensing)
- [ ] ✅ Preserves fixed pipeline sequences (no optionality introduced)
- [ ] ✅ Maintains asset provenance tracking

## Breaking Changes Impact
<!-- If this is a breaking change, describe the impact and migration path -->

### User Impact
- 
- 

### Migration Required
- 
- 

## Checklist
<!-- Ensure all items are completed before requesting review -->

### Code Quality
- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Code is properly commented where necessary
- [ ] No debugging print statements or commented-out code

### Testing  
- [ ] All new/modified code is covered by tests
- [ ] All tests pass locally
- [ ] Tests validate both success and error cases
- [ ] Integration tests verify end-to-end functionality

### Documentation
- [ ] Documentation updated for any API changes
- [ ] README updated if needed
- [ ] Comments added for complex logic
- [ ] Docstrings added/updated for public methods

### Security & Compliance
- [ ] No secrets or API keys committed
- [ ] Security implications reviewed
- [ ] Dependency changes reviewed for vulnerabilities
- [ ] Prompt asset integrity maintained

## Related Issues
<!-- Link any related issues -->
Closes #
Relates to #

## Screenshots/Logs
<!-- Include any relevant screenshots or log output -->

## Additional Notes
<!-- Any additional information that reviewers should know -->

---

## Reviewer Guidelines
<!-- For reviewers: key areas to focus on -->

### Critical Review Areas
1. **Semantic Integrity**: Verify no AI-generated semantic content
2. **API Compliance**: Confirm Responses API usage only  
3. **Architecture**: Validate component-station separation
4. **Testing**: Ensure comprehensive test coverage
5. **Breaking Changes**: Verify compatibility or migration path

### Testing Commands
```bash
# Basic validation
pytest tests/lib/test_strategies.py -v
pytest tests/integration/test_prompt_system_integration.py -v

# CLI smoke test
python -m chirality.cli info
python -m chirality.cli compute-cell C --i 0 --j 0 --resolver echo --verbose

# API compliance check
pytest tests/test_api_compliance.py -v
```