import '@testing-library/jest-dom'

if (!('WebkitAppearance' in document.documentElement.style)) {
    document.documentElement.style['WebkitAppearance'] = ''
}
